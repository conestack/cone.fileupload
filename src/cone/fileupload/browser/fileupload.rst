fileupload server integration tests
===================================

Default i18n messages, upload and download templates::

    >>> from cone.fileupload.browser.fileupload import (
    ...     I18N_MESSAGES,
    ...     UPLOAD_TEMPLATE,
    ...     DOWNLOAD_TEMPLATE,
    ... )

    >>> I18N_MESSAGES
    u'\n<script type="text/javascript">...</script>\n'

    >>> UPLOAD_TEMPLATE
    u'\n<script id="template-upload" type="text/x-tmpl">...</script>\n'

    >>> DOWNLOAD_TEMPLATE
    u'\n<script id="template-download" type="text/x-tmpl">...</script>\n'

Create dummy model::

    >>> from pyramid.security import (
    ...     Everyone,
    ...     Allow,
    ...     Deny,
    ...     ALL_PERMISSIONS,
    ... )
    >>> from cone.app.model import BaseNode

    >>> ACL = [
    ...     (Allow, 'role:manager', ['add', 'delete']),
    ...     (Allow, Everyone, ['login']),
    ...     (Deny, Everyone, ALL_PERMISSIONS),
    ... ]

    >>> class ContainerNode(BaseNode):
    ...     __acl__ = ACL
    ... 
    ...     def __call__(self):
    ...         pass

    >>> container = ContainerNode(name='container')
    >>> container
    <ContainerNode object 'container' at ...>

Render fileupload tile::

    >>> from cone.tile import render_tile

Unauthorized::

    >>> request = layer.new_request()
    >>> render_tile(container, request, 'fileupload')
    Traceback (most recent call last):
      ...
    HTTPForbidden: Unauthorized: 
    tile <cone.fileupload.browser.fileupload.FileUploadTile object at ...> 
    failed permission check

Authorized::

    >>> layer.login('manager')

    >>> request = layer.new_request()
    >>> res = render_tile(container, request, 'fileupload')
    >>> res.find('<form id="fileupload"') > -1
    True

    >>> layer.logout()

Traversable fileupload view::

    >>> from cone.fileupload.browser.fileupload import fileupload

    >>> layer.login('manager')

    >>> request = layer.new_request()
    >>> response = fileupload(container, request)
    >>> response
    <Response at ... 200 OK>

    >>> response.body
    '<!DOCTYPE html PUBLIC...'

    >>> response.body.find('<form id="fileupload"') > -1
    True

    >>> layer.logout()

Abstract file upload handle::

    >>> from cone.fileupload.browser.fileupload import FileUploadHandle

    >>> layer.login('manager')

    >>> request = layer.new_request()
    >>> abstract_upload_handle = FileUploadHandle(container, request)

If request method is GET, existing files are read. Abstract implementation
returns empty result::

    >>> abstract_upload_handle()
    {'files': []}

If request method is POST, a file upload is assumed::

    >>> from StringIO import StringIO
    >>> from cgi import FieldStorage

    >>> filedata = FieldStorage()
    >>> filedata.type = 'text/plain'
    >>> filedata.filename = 'test.txt'
    >>> filedata.file = StringIO('I am the payload')

    >>> request.method = 'POST'
    >>> request.params['file'] = filedata
    >>> del request.params['_LOCALE_']

    >>> res = abstract_upload_handle()
    >>> res['files'][0]['name']
    'test.txt'

    >>> res['files'][0]['size']
    0

    >>> res['files'][0]['error']
    'Abstract ``FileUploadHandle`` does not implement ``create_file``'

Concrete implementation of file upload handle::

    >>> class File(BaseNode):
    ...     __acl__ = ACL
    ...     allow_non_node_childs = True

    >>> class ContainerFileUploadHandle(FileUploadHandle):
    ... 
    ...     def create_file(self, stream, filename, mimetype):
    ...         file = self.model[filename] = File()
    ...         file['body'] = stream.read()
    ...         return {
    ...             'name': filename,
    ...             'size': len(file['body']),
    ...             'url': '/{0}'.format(file.name),
    ...             'deleteUrl': '/{0}/filedelete_handle'.format(file.name),
    ...             'deleteType': 'GET',
    ...         }
    ... 
    ...     def read_existing(self):
    ...         files = list()
    ...         for node in self.model.values():
    ...             files.append({
    ...                 'name': node.name,
    ...                 'size': len(node['body']),
    ...                 'url': '/{0}'.format(node.name),
    ...                 'deleteUrl': '/{0}/filedelete_handle'.format(node.name),
    ...                 'deleteType': 'GET',
    ...             })
    ...         return files

Upload file::

    >>> upload_handle = ContainerFileUploadHandle(container, request)
    >>> res = upload_handle()
    >>> res['files']
    [{'url': '/test.txt', 
    'deleteType': 'GET', 
    'deleteUrl': '/test.txt/filedelete_handle', 
    'name': 'test.txt', 
    'size': 16}]

    >>> container.printtree()
    <class 'ContainerNode'>: container
      <class 'File'>: test.txt
        body: 'I am the payload'

Read existing files::

    >>> request = layer.new_request()
    >>> upload_handle = ContainerFileUploadHandle(container, request)
    >>> upload_handle()['files']
    [{'url': '/test.txt', 
    'deleteType': 'GET', 
    'deleteUrl': '/test.txt/filedelete_handle', 
    'name': 'test.txt', 
    'size': 16}]

Test file delete handle::

    >>> from cone.fileupload.browser.fileupload import filedelete_handle

    >>> file = container['test.txt']
    >>> request = layer.new_request()
    >>> filedelete_handle(file, request)
    {'files': [{'test.txt': True}]}

    >>> container.printtree()
    <class 'ContainerNode'>: container

    >>> layer.logout()
