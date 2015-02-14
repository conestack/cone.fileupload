from pyramid.view import view_config
from pyramid.i18n import TranslationStringFactory
from cone.tile import tile
from cone.app.browser import render_main_template
from cone.app.browser.actions import LinkAction
from cone.app.browser.contextmenu import context_menu
from cone.app.browser.layout import ProtectedContentTile
from cone.app.browser.utils import make_url


_ = TranslationStringFactory('cone.fileupload')


# class FileUploadAction(LinkAction):
#     id = 'toolbaraction-fileupload'
#     css = ''
#     icon = 'toolbaricon-fileupload'
#     title = _('fileupload', default=u'File Upload')
#     action = 'fileupload:#content:inner'
#     href = LinkAction.target
# 
#     @property
#     def display(self):
#         return isinstance(self.model, Slide)
# 
#     @property
#     def selected(self):
#         return self.action_scope == 'fileupload'
# 
# 
# context_menu['contentviews']['fileupload'] = FileUploadAction(True)


@tile('fileupload', 'fileupload.pt', permission='add')
class FileUploadTile(ProtectedContentTile):

    @property
    def upload_url(self):
        return make_url(self.request,
                        node=self.model,
                        resource='fileupload_handler')


@view_config('fileupload', permission='add')
def fileupload(model, request):
    return render_main_template(model, request, 'fileupload')


@view_config(name='fileupload_handler', permission='add')
def fileupload_handler(model, request):
    pass
