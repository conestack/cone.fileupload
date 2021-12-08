from cgi import FieldStorage
from cone.app import testing
from cone.app.model import BaseNode
from cone.fileupload.browser.fileupload import filedelete_handle
from cone.fileupload.browser.fileupload import fileupload
from cone.fileupload.browser.fileupload import FileUploadHandle
from cone.fileupload.browser.fileupload import templates
from cone.tile import render_tile
from cone.tile.tests import TileTestCase
from pyramid.httpexceptions import HTTPForbidden
from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Allow
from pyramid.security import Deny
from pyramid.security import Everyone
try:
    from StringIO import StringIO
except ImportError:  # pragma: no cover
    from io import StringIO
import sys
import unittest


class FileuploadLayer(testing.Security):

    def make_app(self, **kw):
        super(FileuploadLayer, self).make_app(**{
            'cone.plugins': 'cone.fileupload'
        })


ACL = [
    (Allow, 'role:manager', ['add', 'delete']),
    (Allow, Everyone, ['login']),
    (Deny, Everyone, ALL_PERMISSIONS)
]


class ContainerNode(BaseNode):
    __acl__ = ACL

    def __call__(self):
        pass


class File(BaseNode):
    __acl__ = ACL
    allow_non_node_children = True


class ContainerFileUploadHandle(FileUploadHandle):

    def create_file(self, stream, filename, mimetype):
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


class TestFileupload(TileTestCase):
    layer = FileuploadLayer()

    def test_default_templates(self):
        # Default i18n messages, upload and download templates
        self.checkOutput("""
        <script type="text/javascript">...</script>
        """, templates.I18N_MESSAGES)

        self.checkOutput("""
        <script id="template-upload" type="text/x-tmpl">...</script>
        """, templates.UPLOAD_TEMPLATE)

        self.checkOutput("""
        <script id="template-download" type="text/x-tmpl">...</script>
        """, templates.DOWNLOAD_TEMPLATE)

    def test_fileupload_tile(self):
        container = ContainerNode(name='container')

        # Render fileupload tile unauthorized
        request = self.layer.new_request()
        err = self.expectError(
            HTTPForbidden,
            render_tile,
            container,
            request,
            'fileupload'
        )
        self.checkOutput("""
        Unauthorized: tile
        <cone.fileupload.browser.fileupload.FileUploadTile object at ...>
        failed permission check
        """, str(err))

        # Render fileupload tile authorized
        with self.layer.authenticated('manager'):
            res = render_tile(container, request, 'fileupload')
            self.assertTrue(res.find('<form id="fileupload"') > -1)

    def test_fileupload_view(self):
        # Traversable fileupload view
        container = ContainerNode(name='container')
        request = self.layer.new_request()

        with self.layer.authenticated('manager'):
            response = fileupload(container, request)

        self.assertTrue(response.text.startswith('<!DOCTYPE html'))
        self.assertTrue(response.text.find('<form id="fileupload"') > -1)

    def test_fileupload_handle(self):
        # Abstract file upload handle
        container = ContainerNode(name='container')
        request = self.layer.new_request()
        abstract_upload_handle = FileUploadHandle(container, request)

        # If request method is GET, existing files are read. Abstract
        # implementation returns empty result
        self.assertEqual(abstract_upload_handle(), {'files': []})

        # If request method is POST, a file upload is assumed
        filedata = FieldStorage()
        filedata.type = 'text/plain'
        filedata.filename = 'test.txt'
        filedata.file = StringIO('I am the payload')

        request.method = 'POST'
        request.params['file'] = filedata
        del request.params['_LOCALE_']

        res = abstract_upload_handle()
        self.assertEqual(res['files'][0]['name'], 'test.txt')
        self.assertEqual(res['files'][0]['size'], 0)
        self.assertEqual(
            res['files'][0]['error'],
            'Abstract ``FileUploadHandle`` does not implement ``create_file``'
        )

        # Concrete implementation of file upload handle
        upload_handle = ContainerFileUploadHandle(container, request)

        # Upload file
        res = upload_handle()
        self.assertEqual(res['files'], [{
            'name': 'test.txt',
            'size': 16,
            'view_url': '/test.txt',
            'download_url': '/test.txt/download',
            'delete_url': '/test.txt/filedelete_handle',
            'delete_type': 'GET'
        }])

        self.checkOutput("""
        <class 'cone.fileupload.tests.ContainerNode'>: container
          <class 'cone.fileupload.tests.File'>: test.txt
            body: 'I am the payload'
        """, container.treerepr())

        # Read existing files
        request = self.layer.new_request()
        upload_handle = ContainerFileUploadHandle(container, request)
        self.assertEqual(upload_handle()['files'], [{
            'name': 'test.txt',
            'size': 16,
            'view_url': '/test.txt',
            'download_url': '/test.txt/download',
            'delete_url': '/test.txt/filedelete_handle',
            'delete_type': 'GET'
        }])

        # Test file delete handle
        file = container['test.txt']
        request = self.layer.new_request()
        self.assertEqual(
            filedelete_handle(file, request),
            {'files': [{'test.txt': True}]}
        )

        self.checkOutput("""
        <class 'cone.fileupload.tests.ContainerNode'>: container
        """, container.treerepr())


def run_tests():
    from cone.fileupload import tests
    from zope.testrunner.runner import Runner

    suite = unittest.TestSuite()
    suite.addTest(unittest.findTestCases(tests))

    runner = Runner(found_suites=[suite])
    runner.run()
    sys.exit(int(runner.failed))


if __name__ == '__main__':
    run_tests()
