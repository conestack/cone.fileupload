cone.fileupload
===============

This package integrates jQuery File Upload
(https://github.com/blueimp/jQuery-File-Upload/) in cone.

Currently, tag 9.9.3 is included. See
(https://github.com/blueimp/jQuery-File-Upload/releases).


Usage
-----

Since ``cone.app`` not knows about the underlying data, ``cone.fileupload``
only provides an abstract server implementation.

So first we need to provide a model.

.. code-block:: python

    from pyramid.security import (
        Everyone,
        Allow,
        Deny,
        ALL_PERMISSIONS,
    )
    from cone.app.model import BaseNode

    # define an ACL
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
        allow_non_node_childs = True # allow setting any value types

Now we need to provide a concrete ``FileUploadHandle`` implementation for
our model.

.. code-block:: python

    from pyramid.view import view_config
    from cone.fileupload.browser.fileupload import FileUploadHandle

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
                'url': '/{0}'.format(file.name),
                'deleteUrl': '/{0}/filedelete_handle'.format(file.name),
                'deleteType': 'GET',
            }

        def read_existing(self):
            # this function gets called for initial reading of existing files
            files = list()
            for node in self.model.values():
                files.append({
                    'name': node.name,
                    'size': len(node['body']),
                    'url': '/{0}'.format(node.name),
                    'deleteUrl': '/{0}/filedelete_handle'.format(node.name),
                    'deleteType': 'GET',
                })
            return files

Optionally we might want to provide a custom fileupload tile for our model.

.. code-block:: python

    from cone.tile import tile
    from cone.fileupload.browser.fileupload import FileUploadTile

    @tile(
        'fileupload',
        'cone.fileupload:browser/fileupload.pt',
        interface=Container,
        permission='add')
    class ContainerFileUploadTile(FileUploadTile):
        accept_file_types = '/(\.|\/)(gif|jpg)$/i'
        disable_image_preview = True
        disable_video_preview = True
        disable_audio_preview = True


TestCoverage
------------

Summary of the test coverage report::

  lines   cov%   module   (path)
     27   100%   cone.fileupload.__init__
      2   100%   cone.fileupload.browser.__init__
     89   100%   cone.fileupload.browser.fileupload
     18   100%   cone.fileupload.tests


Contributors
============

- Robert Niederreiter <rnix [at] squarewave [dot] at>


Changes
=======

0.1
---

- Make it work
  [rnix]
