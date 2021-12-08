from cone.app.browser import render_main_template
from cone.app.browser.utils import make_url
from cone.fileupload.browser import templates
from cone.tile import Tile
from cone.tile import tile
from pyramid.i18n import get_localizer
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config


_ = TranslationStringFactory('cone.fileupload')


@tile(
    name='fileupload_toolbar',
    path='toolbar.pt',
    permission='add')
class FileUploadToolbarTile(Tile):
    """Tile rendering the file upload toolbar.
    """


@tile(name='fileupload', path='fileupload.pt', permission='add')
class FileUploadTile(Tile):
    """Register this tile for specific context if jQuery file upload settings
    should be customized.
    """
    accept_file_types = ''  # e.g. /(\.|\/)(gif|jpe?g|png)$/i
    i18n_messages_src = templates.I18N_MESSAGES
    upload_template_src = templates.UPLOAD_TEMPLATE
    download_template_src = templates.DOWNLOAD_TEMPLATE

    @property
    def show_contextmenu(self):
        return self.model.properties.fileupload_contextmenu_actions

    @property
    def i18n_messages(self):
        localizer = get_localizer(self.request)
        translate = localizer.translate
        return self.i18n_messages_src.format(
            uploaded_bytes=translate(_(
                'uploaded_bytes',
                default='Uploaded bytes exceed file size'
            )),
            accept_file_types=translate(_(
                'accept_file_types',
                default='File type not allowed'
            ))
        )

    @property
    def upload_template(self):
        localizer = get_localizer(self.request)
        translate = localizer.translate
        return self.upload_template_src.format(
            processing=translate(_('processing', default=u'Processing...')),
            start=translate(_('start', default=u'Start')),
            cancel=translate(_('cancel', default=u'Cancel')),
        )

    @property
    def download_template(self):
        localizer = get_localizer(self.request)
        translate = localizer.translate
        return self.download_template_src.format(
            error=translate(_('error', default=u'Error')),
            delete=translate(_('delete', default=u'Delete')),
            cancel=translate(_('cancel', default=u'Cancel')),
            download=translate(_('download', default=u'Download')),
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
        file data.

        [
            {
                'name': 'pic.jpg',
                'size': 841946,
                'view_url': 'http://example.org/pic.jpg',
                'download_url': 'http://example.org/pic.jpg/download',
                'delete_url': 'http://example.org/pic.jpg/filedelete_handle',
                'delete_type': 'GET',
            }
        ]
        """
        return []

    def create_file(self, stream, filename, mimetype):
        """Create file by uploaded stream and return file data dict.

        {
            'name': 'pic.jpg',
            'size': 841946,
            'view_url': 'http://example.org/pic.jpg',
            'download_url': 'http://example.org/pic.jpg/download',
            'delete_url': 'http://example.org/pic.jpg/filedelete_handle',
            'delete_type': 'GET',
        }
        """
        return {
            'name': filename,
            'size': 0,
            'error': (
                'Abstract ``FileUploadHandle`` does not '
                'implement ``create_file``'
            )
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
