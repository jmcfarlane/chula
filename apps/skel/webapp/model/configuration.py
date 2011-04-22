# Python imports
from os import path

# Project imports
from chula import config

# Application configuration
app = config.Config()
app.classpath = 'controller'
app.debug = True
app.htdocs = path.realpath(path.join(path.dirname(__file__), '..', 'www'))
app.session = False

# Controller routing logic
app.mapper = (
    # For sanity...
    (r'^(home/?)?$', 'home.index'),

    # organize the routes in groups
    (r'^/foo/?$', 'home.foo'),
)
