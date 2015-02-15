import os
import logging
import cone.app


logger = logging.getLogger('cone.fileupload')


# protected CSS
css = cone.app.cfg.css
css.protected.append('fileupload-static/css/jquery.fileupload.css')


# protected JS
js = cone.app.cfg.js
js.protected.append('fileupload-static/js/vendor/tmpl.min.js')
js.protected.append('fileupload-static/js/vendor/load-image.all.min.js')
js.protected.append('fileupload-static/js/vendor/canvas-to-blob.min.js')
js.protected.append('fileupload-static/js/vendor/jquery.blueimp-gallery.min.js')
js.protected.append('fileupload-static/js/jquery.iframe-transport.js')
js.protected.append('fileupload-static/js/jquery.fileupload.js')
js.protected.append('fileupload-static/js/jquery.fileupload-process.js')
js.protected.append('fileupload-static/js/jquery.fileupload-image.js')
js.protected.append('fileupload-static/js/jquery.fileupload-audio.js')
js.protected.append('fileupload-static/js/jquery.fileupload-video.js')
js.protected.append('fileupload-static/js/jquery.fileupload-validate.js')
js.protected.append('fileupload-static/js/jquery.fileupload-ui.js')
js.protected.append('fileupload-static/js/cone.fileupload.js')


# application startup initialization
def initialize_fileupload(config, global_config, local_config):
    # static resources
    config.add_view(
        'cone.fileupload.browser.static_resources',
        name='fileupload-static'
    )

    # scan browser package
    config.scan('cone.fileupload.browser')


cone.app.register_main_hook(initialize_fileupload)
