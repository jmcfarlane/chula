import os

from chula import config

# Development configuration
app = config.Config()
app.classpath = 'controller'
app.debug = True
app.htdocs = os.path.join(os.path.dirname(__file__), '..', 'www')
app.session = False

if 'CHULA_REGEX_MAPPER' in os.environ:
    app.mapper = (
        # Home controller
        (r'^$', 'home.index'),
        (r'^/home/?$', 'home.index'),
        (r'^/home/index/?$', 'home.index'),

        # Sample controller
        (r'^/sample/?$', 'sample.index'),
        (r'^/sample/page/?$', 'sample.page'),

        # Bad imports
        (r'^/bad_import/index/?$',
          'bad_import.index'),

        # Controller raising exceptions
        (r'^/global_exception/index/?$',
          'global_exception.index'),

        # Controller with syntax errors
        (r'^/syntax_exception/index/?$',
          'syntax_exception.index'),

        # Controller with runtime errors
        (r'^/runtime_exception/index/?$',
          'runtime_exception.index'),
    )
