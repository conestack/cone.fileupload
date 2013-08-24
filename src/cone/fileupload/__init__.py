import os
import logging
import cone.app


logger = logging.getLogger('cone.fileupload')


# protected CSS
#cone.app.cfg.css.protected.append(
#    'fileupload-static/jquery-fileupload/css/jquery.fileupload-ui.css')


# application startup initialization
def initialize_fileupload(config, global_config, local_config):
    # static resources
    config.add_view('cone.fileupload.browser.static_resources',
                    name='fileupload-static')
    # scan browser package
    config.scan('cone.fileupload.browser')


cone.app.register_main_hook(initialize_fileupload)
