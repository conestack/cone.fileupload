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
