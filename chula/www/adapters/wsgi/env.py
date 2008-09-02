"""
Manage the environment when python is using wsgi
"""

from cgi import FieldStorage

from chula.www.adapters import env

class Environment(env.BaseEnv):
    def __init__(self, environ):
        super(Environment, self).__init__()

        # Set the required variables from the wsgi environ object
        for key, value in environ.iteritems():
            key = key.replace('.', '_')
            if key in self:
                self[key] = value

        # Set http get or post variables
        self.form = FieldStorage(fp=self.wsgi_input,
                                 environ=environ,
                                 keep_blank_values=1)

        # Add additional variables provided by the base class
        super(Environment, self).extras()
