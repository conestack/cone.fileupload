from cone.app.browser import render_main_template
from cone.app.browser.utils import make_url
from cone.tile import Tile
from cone.tile import tile
from pyramid.i18n import TranslationStringFactory
from pyramid.i18n import get_localizer
from pyramid.view import view_config


_ = TranslationStringFactory('cone.fileupload')


I18N_MESSAGES = u"""
<script type="text/javascript">
    var fileupload_i18n_messages = new Object();
    fileupload_i18n_messages.uploadedBytes = '{uploaded_bytes}';
    fileupload_i18n_messages.acceptFileTypes = '{accept_file_types}';
</script>
"""


UPLOAD_TEMPLATE = u"""
<script id="template-upload" type="text/x-tmpl">
{{% for (var i=0, file; file=o.files[i]; i++) {{ %}}
    <tr class="template-upload fade">
        <td>
            <span class="preview"></span>
        </td>
        <td>
            <p class="name">{{%=file.name%}}</p>
            <strong class="error text-danger"></strong>
        </td>
        <td>
            <p class="size">{processing}</p>
            <div class="progress progress-striped active"
                 role="progressbar"
                 aria-valuemin="0"
                 aria-valuemax="100"
                 aria-valuenow="0">
                <div class="progress-bar progress-bar-success"
                     style="width:0%;">
                </div>
            </div>
        </td>
        <td>
            {{% if (!i && !o.options.autoUpload) {{ %}}
                <button class="btn btn-primary start" disabled>
                    <i class="glyphicon glyphicon-upload"></i>
                    <span>{start}</span>
                </button>
            {{% }} %}}
            {{% if (!i) {{ %}}
                <button class="btn btn-warning cancel">
                    <i class="glyphicon glyphicon-ban-circle"></i>
                    <span>{cancel}</span>
                </button>
            {{% }} %}}
        </td>
    </tr>
{{% }} %}}
</script>
"""


DOWNLOAD_TEMPLATE = u"""
<script id="template-download" type="text/x-tmpl">
{{% for (var i=0, file; file=o.files[i]; i++) {{ %}}
    <tr class="template-download fade">
        <td>
            <span class="preview">
                {{% if (file.thumbnailUrl) {{ %}}
                    <a href="{{%=file.url%}}"
                       title="{{%=file.name%}}"
                       download="{{%=file.name%}}"
                       data-gallery><img src="{{%=file.thumbnailUrl%}}"></a>
                {{% }} %}}
            </span>
        </td>
        <td>
            <p class="name">
                {{% if (file.url) {{ %}}
                    <a href="{{%=file.url%}}"
                       title="{{%=file.name%}}"
                       download="{{%=file.name%}}"
                       {{%=file.thumbnailUrl?'data-gallery':''%}}>
                        {{%=file.name%}}
                    </a>
                {{% }} else {{ %}}
                    <span>{{%=file.name%}}</span>
                {{% }} %}}
            </p>
            {{% if (file.error) {{ %}}
                <div>
                  <span class="label label-danger">{error}</span>
                  {{%=file.error%}}
                </div>
            {{% }} %}}
        </td>
        <td>
            <span class="size">{{%=o.formatFileSize(file.size)%}}</span>
        </td>
        <td>
            {{% if (file.deleteUrl) {{ %}}
                <button class="btn btn-danger delete"
                        data-type="{{%=file.deleteType%}}"
                        data-url="{{%=file.deleteUrl%}}"
                        {{% if (file.deleteWithCredentials) {{ %}}
                        data-xhr-fields='{{"withCredentials":true}}'
                        {{% }} %}}>
                    <i class="glyphicon glyphicon-trash"></i>
                    <span>{delete}</span>
                </button>
                <input type="checkbox" name="delete" value="1" class="toggle">
            {{% }} else {{ %}}
                <button class="btn btn-warning cancel">
                    <i class="glyphicon glyphicon-ban-circle"></i>
                    <span>{cancel}</span>
                </button>
            {{% }} %}}
        </td>
    </tr>
{{% }} %}}
</script>
"""


@tile(name='fileupload', path='fileupload.pt', permission='add')
class FileUploadTile(Tile):
    """Register this tile for specific context if jQuery file upload settings
    should be customized.
    """
    accept_file_types = ''  # e.g. /(\.|\/)(gif|jpe?g|png)$/i
    disable_image_preview = False
    disable_video_preview = False
    disable_audio_preview = False

    @property
    def i18n_messages(self):
        localizer = get_localizer(self.request)
        translate = localizer.translate
        return I18N_MESSAGES.format(
            uploaded_bytes=translate(
                _('uploaded_bytes',
                  default='Uploaded bytes exceed file size')),
            accept_file_types=translate(
                _('accept_file_types',
                  default='File type not allowed')),
        )

    @property
    def upload_template(self):
        localizer = get_localizer(self.request)
        translate = localizer.translate
        return UPLOAD_TEMPLATE.format(
            processing=translate(_('processing', default='Processing...')),
            start=translate(_('start', default='Start')),
            cancel=translate(_('cancel', default='Cancel')),
        )

    @property
    def download_template(self):
        localizer = get_localizer(self.request)
        translate = localizer.translate
        return DOWNLOAD_TEMPLATE.format(
            error=translate(_('error', default='Error')),
            delete=translate(_('delete', default='Delete')),
            cancel=translate(_('cancel', default='Cancel')),
        )

    @property
    def upload_url(self):
        return make_url(
            self.request,
            node=self.model,
            resource='fileupload_handle'
        )


@view_config(name='fileupload', permission='add')
def fileupload(model, request):
    """Fileupload as traversable view.
    """
    return render_main_template(model, request, 'fileupload')


# unknown mimetype marker
UNKNOWN_MIMETYPE = object()


@view_config(
    name='fileupload_handle',
    accept='application/json',
    renderer='json',
    permission='add')
class FileUploadHandle(object):
    """Abstract file upload handle.

    Subclass this object and register ``fileupload_handle`` tile for specific
    context.

    Methods ``read_existing`` and ``create_file`` are supposed to be
    implemented on deriving object.
    """

    def __init__(self, model, request):
        self.model = model
        self.request = request

    def __call__(self):
        result = dict()
        # initial reading
        if self.request.method == 'GET':
            result['files'] = self.read_existing()
        # file upload
        elif self.request.method == 'POST':
            result['files'] = list()
            for filedata in self.request.params.values():
                mimetype = filedata.type or UNKNOWN_MIMETYPE
                filename = filedata.filename
                stream = filedata.file
                res = self.create_file(stream, filename, mimetype)
                result['files'].append(res)
        return result

    def read_existing(self):
        """Read existing files in context and return a list of dicts containing
        client data.

        [
            {
                'name': 'pic.jpg',
                'size': 841946,
                'url': 'http://example.org/pic.jpg',
                'thumbnailUrl': 'http://example.org/thumbnail/pic.jpg',
                'deleteUrl': 'http://example.org/pic.jpg/filedelete_handle',
                'deleteType': 'GET',
            }
        ]
        """
        return []

    def create_file(self, stream, filename, mimetype):
        """Create file by uploaded stream and return client data dict.

        {
            'name': 'pic.jpg',
            'size': 841946,
            'url': 'http://example.org/pic.jpg',
            'thumbnailUrl': 'http://example.org/thumbnail/pic.jpg',
            'deleteUrl': 'http://example.org/pic.jpg/filedelete_handle',
            'deleteType': 'GET',
        }
        """
        return {
            'name': filename,
            'size': 0,
            'error': 'Abstract ``FileUploadHandle`` does not implement ' +
                     '``create_file``'
        }


@view_config(
    name='filedelete_handle',
    accept='application/json',
    renderer='json',
    permission='delete')
def filedelete_handle(model, request):
    """Delete file and return client data.

    {
        'files': [{
            'pic.jpg': True
        }]
    }
    """
    parent = model.parent
    name = model.name
    del parent[name]
    parent()
    return {'files': [{name: True}]}
