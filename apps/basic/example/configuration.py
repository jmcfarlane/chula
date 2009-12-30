import os

from chula import config

# Development configuration
dev = config.Config()
dev.classpath = 'example.www.controllers'
dev.construction_controller = 'error'
dev.construction_trigger = '/tmp/chula_example.stop'
dev.debug = True
dev.error_controller = 'error'
dev.session = False

if 'CHULA_REGEX_MAPPER' in os.environ:
    dev.mapper = (
        # Home controller
        (r'^$', 'home.index'),
        (r'^/home/?$', 'home.index'),
        (r'^/home/index/?$', 'home.index'),

        # Sample controller
        (r'^/sample/?$', 'sample.index'),
        (r'^/sample/page/?$', 'sample.page'),
        
        # Bad imports
        (r'^/imports/bad_import/index/?$',
          'imports.bad_import.index'),

        # Controller raising exceptions
        (r'^/imports/global_exception/index/?$',
          'imports.global_exception.index'),

        # Controller with syntax errors
        (r'^/imports/syntax_exception/index/?$',
          'imports.syntax_exception.index'),
    )
