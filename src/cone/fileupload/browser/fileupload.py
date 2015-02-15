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
