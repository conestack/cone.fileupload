from pyramid.view import view_config
from pyramid.i18n import TranslationStringFactory
from cone.tile import tile
from cone.app.browser.actions import LinkAction
from cone.app.browser.contextmenu import context_menu
from cone.app.browser.layout import ProtectedContentTile
from cone.app.browser.utils import make_url
from ..model import Slide

_ = TranslationStringFactory('cone.fileupload')


class FileUploadAction(LinkAction):
    id = 'toolbaraction-fileupload'
    css = ''
    icon = 'toolbaricon-fileupload'
    title = _('fileupload', default=u'File Upload')
    action = 'fileupload:#content:inner'
    href = LinkAction.target

    @property
    def display(self):
        return isinstance(self.model, Slide)

    @property
    def selected(self):
        return self.action_scope == 'fileupload'


#context_menu['contentviews']['fileupload'] = FileUploadAction(True)


@tile('fileupload', 'templates/fileupload.pt',
      interface=Slide, permission='view')
class FileUploadTile(ProtectedContentTile):

    @property
    def upload_url(self):
        return make_url(self.request,
                        node=self.model,
                        resource='fileupload_handler')


@view_config(name='fileupload_handler', context=Slide, permission='view')
def fileupload_handler(model, request):
    pass
