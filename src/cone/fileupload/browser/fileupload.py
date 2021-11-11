from cone.app.browser import render_main_template
from cone.app.browser.utils import make_url
from cone.fileupluad.browser.templates import DOWNLOAD_TEMPLATE
from cone.fileupluad.browser.templates import I18N_MESSAGES
from cone.fileupluad.browser.templates import UPLOAD_TEMPLATE
from cone.tile import Tile
from cone.tile import tile
from pyramid.i18n import get_localizer
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config


_ = TranslationStringFactory('cone.fileupload')


@tile(
    name='fileupload_toolbar',
    path='fileupload_toolbar.pt',
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

    @property
    def show_contextmenu(self):
        return self.model.properties.fileupload_contextmenu_actions

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
