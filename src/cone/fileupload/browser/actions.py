from cone.app.browser.actions import Action
from cone.app.browser.actions import ButtonAction
from cone.app.browser.actions import LinkAction
from cone.app.browser.contextmenu import context_menu_item
from pyramid.i18n import get_localizer
from pyramid.i18n import TranslationStringFactory


_ = TranslationStringFactory('cone.fileupload')


@context_menu_item(group='childactions', name='add_files')
class ActionAddFiles(LinkAction):
    id = 'toolbaraction-add-files'
    icon = 'glyphicon glyphicon-plus'
    text = _('action_add_files', default='Add files')
    bind = None
    target = None

    @property
    def display(self):
        return (
            self.model.properties.fileupload_contextmenu_actions
            and self.permitted('add')
        )


@context_menu_item(group='childactions', name='start_upload')
class ActionStartUpload(ButtonAction):
    id = 'toolbaraction-start-upload'
    icon = 'glyphicon glyphicon-upload'
    text = _('action_start_upload', default='Start Upload')
    css = 'start'
    bind = None
    target = None

    @property
    def display(self):
        return (
            self.model.properties.fileupload_contextmenu_actions
            and self.permitted('add')
        )


@context_menu_item(group='childactions', name='cancel_upload')
class ActionCancelUpload(ButtonAction):
    id = 'toolbaraction-cancel-upload'
    icon = 'glyphicon glyphicon-ban-circle'
    text = _('action_cancel_upload', default='Cancel Upload')
    css = 'cancel'
    bind = None
    target = None

    @property
    def display(self):
        return (
            self.model.properties.fileupload_contextmenu_actions
            and self.permitted('add')
        )


@context_menu_item(group='childactions', name='delete_files')
class ActionDeleteFiles(ButtonAction):
    id = 'toolbaraction-delete-files'
    icon = 'glyphicon glyphicon-trash'
    text = _('action_delete_files', default='Delete Files')
    css = 'delete'
    bind = None
    target = None

    @property
    def display(self):
        return (
            self.model.properties.fileupload_contextmenu_actions
            and self.permitted('delete')
        )


@context_menu_item(group='contextactions', name='select_files')
class ActionSelectFiles(Action):
    id = 'toolbaraction-select-files'
    text = _('action_select_files', default='Select Files')

    @property
    def display(self):
        return (
            self.model.properties.fileupload_contextmenu_actions
            and self.permitted('delete')
        )

    def render(self):
        localizer = get_localizer(self.request)
        return (
            u'<li class="select-files-action">'
            u'  <span>{}<input type="checkbox" class="toggle" /></span>'
            u'</li>'
        ).format(
            localizer.translate(self.text)
        )
