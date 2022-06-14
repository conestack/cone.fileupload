from cgi import FieldStorage
from cone.app import testing
from cone.app.model import BaseNode
from cone.fileupload import browser
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
import os
import sys
import unittest


class FileuploadLayer(testing.Security):

    def make_app(self, **kw):
        super(FileuploadLayer, self).make_app(**{
            'cone.plugins': 'cone.fileupload'
        })


fileupload_layer = FileuploadLayer()


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

    child_constraints = None


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
    layer = fileupload_layer

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


def np(path):
    return path.replace('/', os.path.sep)


class TestResources(unittest.TestCase):
    layer = fileupload_layer

    def test_jquery_fileupload_resources(self):
        resources_ = browser.jquery_fileupload_resources
        self.assertTrue(resources_.directory.endswith(np('/static/jquery-fileupload')))
        self.assertEqual(resources_.name, 'cone.fileupload-jquery-fileupload')
        self.assertEqual(resources_.path, 'jquery-fileupload')

        scripts = resources_.scripts
        self.assertEqual(len(scripts), 7)

        self.assertTrue(scripts[0].directory.endswith(np('/static/jquery-fileupload/vendor')))
        self.assertEqual(scripts[0].path, 'jquery-fileupload/vendor')
        self.assertEqual(scripts[0].file_name, 'tmpl.min.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        self.assertTrue(scripts[1].directory.endswith(np('/static/jquery-fileupload/vendor')))
        self.assertEqual(scripts[1].path, 'jquery-fileupload/vendor')
        self.assertEqual(scripts[1].file_name, 'jquery.ui.widget.js')
        self.assertTrue(os.path.exists(scripts[1].file_path))

        self.assertTrue(scripts[2].directory.endswith(np('/static/jquery-fileupload')))
        self.assertEqual(scripts[2].path, 'jquery-fileupload')
        self.assertEqual(scripts[2].file_name, 'jquery.iframe-transport.js')
        self.assertTrue(os.path.exists(scripts[2].file_path))

        self.assertTrue(scripts[3].directory.endswith(np('/static/jquery-fileupload')))
        self.assertEqual(scripts[3].path, 'jquery-fileupload')
        self.assertEqual(scripts[3].file_name, 'jquery.fileupload.js')
        self.assertTrue(os.path.exists(scripts[3].file_path))

        self.assertTrue(scripts[4].directory.endswith(np('/static/jquery-fileupload')))
        self.assertEqual(scripts[4].path, 'jquery-fileupload')
        self.assertEqual(scripts[4].file_name, 'jquery.fileupload-process.js')
        self.assertTrue(os.path.exists(scripts[4].file_path))

        self.assertTrue(scripts[5].directory.endswith(np('/static/jquery-fileupload')))
        self.assertEqual(scripts[5].path, 'jquery-fileupload')
        self.assertEqual(scripts[5].file_name, 'jquery.fileupload-validate.js')
        self.assertTrue(os.path.exists(scripts[5].file_path))

        self.assertTrue(scripts[6].directory.endswith(np('/static/jquery-fileupload')))
        self.assertEqual(scripts[6].path, 'jquery-fileupload')
        self.assertEqual(scripts[6].file_name, 'jquery.fileupload-ui.js')
        self.assertTrue(os.path.exists(scripts[6].file_path))

        styles = resources_.styles
        self.assertEqual(len(styles), 1)

        self.assertTrue(styles[0].directory.endswith(np('/static/jquery-fileupload')))
        self.assertEqual(styles[0].path, 'jquery-fileupload')
        self.assertEqual(styles[0].file_name, 'jquery.fileupload.css')
        self.assertTrue(os.path.exists(styles[0].file_path))

    def test_cone_fileupload_resources(self):
        resources_ = browser.cone_fileupload_resources
        self.assertTrue(resources_.directory.endswith(np('/static/fileupload')))
        self.assertEqual(resources_.name, 'cone.fileupload-fileupload')
        self.assertEqual(resources_.path, 'fileupload')

        scripts = resources_.scripts
        self.assertEqual(len(scripts), 1)

        self.assertTrue(scripts[0].directory.endswith(np('/static/fileupload')))
        self.assertEqual(scripts[0].path, 'fileupload')
        self.assertEqual(scripts[0].file_name, 'cone.fileupload.min.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        styles = resources_.styles
        self.assertEqual(len(styles), 1)

        self.assertTrue(styles[0].directory.endswith(np('/static/fileupload')))
        self.assertEqual(styles[0].path, 'fileupload')
        self.assertEqual(styles[0].file_name, 'cone.fileupload.css')
        self.assertTrue(os.path.exists(styles[0].file_path))


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
