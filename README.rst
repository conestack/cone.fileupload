.. image:: https://img.shields.io/pypi/v/cone.fileupload.svg
    :target: https://pypi.python.org/pypi/cone.fileupload
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/cone.fileupload.svg
    :target: https://pypi.python.org/pypi/cone.fileupload
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/bluedynamics/cone.fileupload.svg?branch=master
    :target: https://travis-ci.org/bluedynamics/cone.fileupload

.. image:: https://coveralls.io/repos/github/bluedynamics/cone.fileupload/badge.svg?branch=master
    :target: https://coveralls.io/github/bluedynamics/cone.fileupload?branch=master

This package integrates
`jQueryFileUpload <https://github.com/blueimp/jQuery-File-Upload>`_ in cone.

Currently, version 10.32.0 is included.

Included files of jQuery File Upload:

* jquery.iframe-transport.js
* jquery.fileupload.js
* jquery.fileupload-process.js
* jquery.fileupload-ui.js
* jquery.fileupload-validate.js

Additionally, v3.20.0 of
`Javascript-Templates <https://github.com/blueimp/JavaScript-Templates>`_
is included.


Usage
-----

Since ``cone.app`` not knows about the underlying data, ``cone.fileupload``
only provides an abstract server implementation.

So first we need to provide a model.

.. code-block:: python

    from cone.app.model import BaseNode
    from pyramid.security import ALL_PERMISSIONS
    from pyramid.security import Allow
    from pyramid.security import Deny
    from pyramid.security import Everyone

    ACL = [
        (Allow, 'role:manager', ['add', 'delete']),
        (Allow, Everyone, ['login']),
        (Deny, Everyone, ALL_PERMISSIONS),
    ]

    class Container(BaseNode):
        __acl__ = ACL

        def __call__(self):
            """Persistence happens here.
            """

    class File(BaseNode):
        __acl__ = ACL

        # allow setting any value types
        child_constraints = None

Now we need to provide a concrete ``FileUploadHandle`` implementation for
our model.

.. code-block:: python

    from cone.fileupload.browser.fileupload import FileUploadHandle
    from pyramid.view import view_config

    @view_config(
        name='fileupload_handle',
        context=Container, # <- here the view gets bound to our model
        accept='application/json',
        renderer='json',
        permission='add')
    class ContainerFileUploadHandle(FileUploadHandle):

        def create_file(self, stream, filename, mimetype):
            # this function gets called for persisting uploaded files
            file = self.model[filename] = File()
            file['body'] = stream.read()
            return {
                'name': filename,
                'size': len(file['body']),
                'view_url': '/{0}'.format(file.name),
                'download_url': '/{0}/download'.format(file.name),
                'delete_url': '/{0}/filedelete_handle'.format(file.name),
                'delete_type': 'GET',
            }

        def read_existing(self):
            # this function gets called for initial reading of existing files
            files = list()
            for node in self.model.values():
                files.append({
                    'name': node.name,
                    'size': len(node['body']),
                    'view_url': '/{0}'.format(node.name),
                    'download_url': '/{0}/download'.format(node.name),
                    'delete_url': '/{0}/filedelete_handle'.format(node.name),
                    'delete_type': 'GET',
                })
            return files

Optionally we might want to provide a custom fileupload tile for our model.

.. code-block:: python

    from cone.tile import tile
    from cone.fileupload.browser.fileupload import FileUploadTile

    @tile(
        name='fileupload',
        path='cone.fileupload:browser/fileupload.pt',
        interface=Container,
        permission='add')
    class ContainerFileUploadTile(FileUploadTile):
        accept_file_types = r'/(\.|\/)(gif|jpg)$/i'

The file upload actions are either rendered as dedicated tile by name
``fileupload_toolbar`` or integrated into the context menu. If it's desired to
display the action in the context menu, ``fileupload_contextmenu_actions``
flag must be set on model ``properties``.


Contributors
============

- Robert Niederreiter
