"""
Manage the environment when python is using wsgi
"""

from cgi import FieldStorage

from chula.www.adapters import env

class Environment(env.BaseEnv):
    def __init__(self, environ):
        super(Environment, self).__init__()
        
        # Indicate what type of adapter this is
        self.chula_adapter = 'wsgi'

        # Set the required variables from the wsgi environ object
        self.fill(environ)

        # Check for redirects and recover the querystring
        if 'REDIRECT_QUERY_STRING' in environ:
            self.QUERY_STRING = environ.get('REDIRECT_QUERY_STRING')

        # Set http get or post variables
        self.form = FieldStorage(fp=self.wsgi_input,
                                 environ=environ,
                                 keep_blank_values=1)

        # Add additional variables provided by the base class
        super(Environment, self).extras()
