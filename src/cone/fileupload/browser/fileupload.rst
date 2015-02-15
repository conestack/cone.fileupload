fileupload server integration tests
===================================

Default upload and download templates::

    >>> from cone.fileupload.browser.fileupload import (
    ...     UPLOAD_TEMPLATE,
    ...     DOWNLOAD_TEMPLATE,
    ... )

    >>> UPLOAD_TEMPLATE
    '\n<script id="template-upload" type="text/x-tmpl">...</script>\n'

    >>> DOWNLOAD_TEMPLATE
    '\n<script id="template-download" type="text/x-tmpl">...</script>\n'
