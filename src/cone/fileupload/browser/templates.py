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
          <p class="name m-0">{{%=file.name%}}</p>
        </td>
        <td>
            <p class="size">{processing}</p>
            <div class="progress border border-primary active w-100"
                 role="progressbar"
                 aria-valuemin="0"
                 aria-valuemax="100"
                 aria-valuenow="0">
                <div class="progress-bar progress-bar-striped progress-bar-animated h-100"
                     style="width:0%;">
                </div>
            </div>
        </td>
        <td class="file_actions">
            {{% if (!i && !o.options.autoUpload) {{ %}}
                <button class="btn btn-primary start" disabled>
                    <i class="bi bi-upload"></i>
                    <span>{start}</span>
                </button>
            {{% }} %}}
            {{% if (!i) {{ %}}
                <button class="btn btn-warning cancel">
                    <i class="bi bi-x-circle"></i>
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
            <p class="name m-0" data-filename="{{%=file.name%}}">
                <a href="{{%=file.view_url%}}"
                   title="{{%=file.name%}}"
                   onclick="cone_fileupload.show_file(event, '{{%=file.view_url%}}');">
                    {{%=file.name%}}
                </a>
            </p>
            {{% if (file.error) {{ %}}
                <div class="alert alert-danger m-0 mt-1 px-2 py-1">
                  <i class="bi bi-x-octagon me-1"></i>
                  <span>{error}</span>:
                  {{%=file.error%}}
                </div>
            {{% }} %}}
        </td>
        <td>
            <span class="size">{{%=o.formatFileSize(file.size)%}}</span>
        </td>
        <td class="file_actions">
            {{% if (file.download_url) {{ %}}
                <a class="btn btn-primary download"
                   href="{{%=file.download_url%}}"
                   title="{{%=file.name%}}"
                   download="{{%=file.name%}}">
                  <i class="bi bi-download"></i>
                  <span>{download}</span>
                </a>
            {{% }} %}}
            {{% if (file.delete_url) {{ %}}
                <button class="btn btn-danger delete"
                        data-type="{{%=file.delete_type%}}"
                        data-url="{{%=file.delete_url%}}"
                        {{% if (file.deleteWithCredentials) {{ %}}
                        data-xhr-fields='{{"withCredentials":true}}'
                        {{% }} %}}>
                    <i class="bi bi-trash"></i>
                    <span>{delete}</span>
                </button>
                <input type="checkbox"
                       class="mx-2 d-inline-block form-check"
                       name="delete" value="1" class="toggle">
            {{% }} else {{ %}}
                <button class="btn btn-warning cancel">
                    <i class="bi bi-x-circle"></i>
                    <span>{cancel}</span>
                </button>
            {{% }} %}}
        </td>
    </tr>
{{% }} %}}
</script>
"""
