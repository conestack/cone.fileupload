from cone.app import main_hook
from cone.app.browser import configure_resources
import logging


logger = logging.getLogger('cone.fileupload')


@main_hook
def initialize_fileupload(config, global_config, settings):
    # application startup initialization

    # static resources
    configure_resources(settings)

    # add translation
    config.add_translation_dirs('cone.fileupload:locale/')

    # scan browser package
    config.scan('cone.fileupload.browser')
