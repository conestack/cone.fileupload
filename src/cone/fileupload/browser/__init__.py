import webresource as wr
import os


resources_dir = os.path.join(os.path.dirname(__file__), 'static')

# jquery fileupload
jquery_fileupload_resources = wr.ResourceGroup(
    name='cone.fileupload-jquery-fileupload',
    directory=os.path.join(resources_dir, 'jquery-fileupload'),
    path='jquery-fileupload'
)
jquery_fileupload_resources.add(wr.ScriptResource(
    name='blueimp-tmpl-js',
    directory=os.path.join(resources_dir, 'jquery-fileupload', 'vendor'),
    path='jquery-fileupload/vendor',
    resource='tmpl.min.js'
))
jquery_fileupload_resources.add(wr.ScriptResource(
    name='jquery-ui-widget-js',
    depends='jquery-js',
    directory=os.path.join(resources_dir, 'jquery-fileupload', 'vendor'),
    path='jquery-fileupload/vendor',
    resource='jquery.ui.widget.js'
))
jquery_fileupload_resources.add(wr.ScriptResource(
    name='jquery-fileupload-iframe-transport-js',
    depends='jquery-js',
    resource='jquery.iframe-transport.js'
))
jquery_fileupload_resources.add(wr.ScriptResource(
    name='jquery-fileupload-js',
    depends='jquery-ui-widget-js',
    resource='jquery.fileupload.js'
))
jquery_fileupload_resources.add(wr.ScriptResource(
    name='jquery-fileupload-process-js',
    depends='jquery-fileupload-js',
    resource='jquery.fileupload-process.js'
))
jquery_fileupload_resources.add(wr.ScriptResource(
    name='jquery-fileupload-validate-js',
    depends='jquery-fileupload-process-js',
    resource='jquery.fileupload-validate.js'
))
jquery_fileupload_resources.add(wr.ScriptResource(
    name='jquery-fileupload-ui-js',
    depends=[
        'blueimp-tmpl-js',
        'jquery-fileupload-validate-js'
    ],
    resource='jquery.fileupload-ui.js'
))
jquery_fileupload_resources.add(wr.StyleResource(
    name='jquery-fileupload-css',
    resource='jquery.fileupload.css'
))

# cone fileupload
cone_fileupload_resources = wr.ResourceGroup(
    name='cone.fileupload-fileupload',
    directory=os.path.join(resources_dir, 'fileupload'),
    path='fileupload'
)
cone_fileupload_resources.add(wr.ScriptResource(
    name='cone-fileupload-js',
    depends='jquery-fileupload-ui-js',
    resource='cone.fileupload.js',
    compressed='cone.fileupload.min.js'
))
cone_fileupload_resources.add(wr.StyleResource(
    name='cone-fileupload-css',
    depends='jquery-fileupload-css',
    resource='cone.fileupload.css'
))


def configure_resources(config, settings):
    # jquery fileupload
    config.register_resource(jquery_fileupload_resources)
    config.set_resource_include('blueimp-tmpl-js', 'authenticated')
    config.set_resource_include('jquery-ui-widget-js', 'authenticated')
    config.set_resource_include('jquery-fileupload-iframe-transport-js', 'authenticated')
    config.set_resource_include('jquery-fileupload-js', 'authenticated')
    config.set_resource_include('jquery-fileupload-process-js', 'authenticated')
    config.set_resource_include('jquery-fileupload-validate-js', 'authenticated')
    config.set_resource_include('jquery-fileupload-ui-js', 'authenticated')
    config.set_resource_include('jquery-fileupload-css', 'authenticated')

    # cone fileupload
    config.register_resource(cone_fileupload_resources)
    config.set_resource_include('cone-fileupload-js', 'authenticated')
    config.set_resource_include('cone-fileupload-css', 'authenticated')
