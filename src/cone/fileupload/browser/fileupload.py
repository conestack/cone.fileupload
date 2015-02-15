from pyramid.view import view_config
from pyramid.i18n import TranslationStringFactory
from cone.tile import tile
from cone.app.browser import render_main_template
from cone.app.browser.layout import ProtectedContentTile
from cone.app.browser.utils import make_url


_ = TranslationStringFactory('cone.fileupload')


UPLOAD_TEMPLATE = """
<script id="template-upload" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-upload fade">
        <td>
            <span class="preview"></span>
        </td>
        <td>
            <p class="name">{%=file.name%}</p>
            <strong class="error text-danger"></strong>
        </td>
        <td>
            <p class="size">Processing...</p>
            <div class="progress progress-striped active" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="progress-bar progress-bar-success" style="width:0%;"></div></div>
        </td>
        <td>
            {% if (!i && !o.options.autoUpload) { %}
                <button class="btn btn-primary start" disabled>
                    <i class="glyphicon glyphicon-upload"></i>
                    <span>Start</span>
                </button>
            {% } %}
            {% if (!i) { %}
                <button class="btn btn-warning cancel">
                    <i class="glyphicon glyphicon-ban-circle"></i>
                    <span>Cancel</span>
                </button>
            {% } %}
        </td>
    </tr>
{% } %}
</script>
"""


DOWNLOAD_TEMPLATE = """
<script id="template-download" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-download fade">
        <td>
            <span class="preview">
                {% if (file.thumbnailUrl) { %}
                    <a href="{%=file.url%}" title="{%=file.name%}" download="{%=file.name%}" data-gallery><img src="{%=file.thumbnailUrl%}"></a>
                {% } %}
            </span>
        </td>
        <td>
            <p class="name">
                {% if (file.url) { %}
                    <a href="{%=file.url%}" title="{%=file.name%}" download="{%=file.name%}" {%=file.thumbnailUrl?'data-gallery':''%}>{%=file.name%}</a>
                {% } else { %}
                    <span>{%=file.name%}</span>
                {% } %}
            </p>
            {% if (file.error) { %}
                <div><span class="label label-danger">Error</span> {%=file.error%}</div>
            {% } %}
        </td>
        <td>
            <span class="size">{%=o.formatFileSize(file.size)%}</span>
        </td>
        <td>
            {% if (file.deleteUrl) { %}
                <button class="btn btn-danger delete" data-type="{%=file.deleteType%}" data-url="{%=file.deleteUrl%}"{% if (file.deleteWithCredentials) { %} data-xhr-fields='{"withCredentials":true}'{% } %}>
                    <i class="glyphicon glyphicon-trash"></i>
                    <span>Delete</span>
                </button>
                <input type="checkbox" name="delete" value="1" class="toggle">
            {% } else { %}
                <button class="btn btn-warning cancel">
                    <i class="glyphicon glyphicon-ban-circle"></i>
                    <span>Cancel</span>
                </button>
            {% } %}
        </td>
    </tr>
{% } %}
</script>
"""


@tile('fileupload', 'fileupload.pt', permission='add')
class FileUploadTile(ProtectedContentTile):
    upload_template = UPLOAD_TEMPLATE
    download_template = DOWNLOAD_TEMPLATE
    accept_file_types = '' # e.g. /(\.|\/)(gif|jpe?g|png)$/i

    @property
    def upload_url(self):
        return make_url(
            self.request,
            node=self.model,
            resource='fileupload_handle'
        )


@view_config('fileupload', permission='add')
def fileupload(model, request):
    return render_main_template(model, request, 'fileupload')


UNKNOWN_MIMETYPE = object()


@view_config(
    name='fileupload_handle',
    accept='application/json',
    renderer='json',
    permission='add')
class FileUploadHandle(object):

    def __init__(self, model, request):
        self.model = model
        self.request = request

    def __call__(self):
        result = dict()
        result['files'] = self.read_existing()
        for filedata in self.request.params.values():
            mimetype = filedata.type or UNKNOWN_MIMETYPE
            filename = filedata.filename
            stream = filedata.file
            if stream:
                stream.seek(0, 2)
                size = stream.tell()
                stream.seek(0)
            else:
                result['files'].append({
                    'name': filename,
                    'size': 0,
                    'error': 'No upload stream'
                })
                continue
            result['files'].append(
                self.create_file(stream, filename, mimetype)
            )
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
                'deleteUrl': 'http://example.org/pic.jpg',
                'deleteType': 'POST',
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
            'deleteUrl': 'http://example.org/pic.jpg',
            'deleteType': 'POST',
        }
        """
        return {
            'name': filename,
            'size': 0,
            'error': 'Abstract ``FileUploadHandle`` does not implement ' +\
                     '``create_file``'
        }


@view_config(
    name='filedelete_handle',
    accept='application/json',
    renderer='json',
    permission='delete')
def filedelete_handle(model, request):
    pass
