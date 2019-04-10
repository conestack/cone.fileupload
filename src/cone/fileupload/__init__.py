from cone.app import cfg
from cone.app import main_hook
from cone.fileupload.browser import static_resources
import logging


logger = logging.getLogger('cone.fileupload')


@main_hook
def initialize_fileupload(config, global_config, settings):
    # application startup initialization

    # protected CSS
    cfg.css.protected.append('fileupload-static/css/jquery.fileupload.css')

    # protected JS
    cfg.js.protected.append('fileupload-static/js/vendor/tmpl.min.js')
    cfg.js.protected.append('fileupload-static/js/vendor/load-image.all.min.js')
    cfg.js.protected.append('fileupload-static/js/vendor/canvas-to-blob.min.js')
    cfg.js.protected.append('fileupload-static/js/vendor/jquery.blueimp-gallery.min.js')  # noqa
    cfg.js.protected.append('fileupload-static/js/jquery.iframe-transport.js')
    cfg.js.protected.append('fileupload-static/js/jquery.fileupload.js')
    cfg.js.protected.append('fileupload-static/js/jquery.fileupload-process.js')
    cfg.js.protected.append('fileupload-static/js/jquery.fileupload-image.js')
    cfg.js.protected.append('fileupload-static/js/jquery.fileupload-audio.js')
    cfg.js.protected.append('fileupload-static/js/jquery.fileupload-video.js')
    cfg.js.protected.append('fileupload-static/js/jquery.fileupload-validate.js')
    cfg.js.protected.append('fileupload-static/js/jquery.fileupload-ui.js')
    cfg.js.protected.append('fileupload-static/js/cone.fileupload.js')

    # add translation
    config.add_translation_dirs('cone.fileupload:locale/')

    # static resources
    config.add_view(static_resources, name='fileupload-static')

    # scan browser package
    config.scan('cone.fileupload.browser')
