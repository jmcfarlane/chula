"""
Manage the environment when python is using wsgi
"""

from cgi import FieldStorage as FS

from chula.www.adapters import env

class Environment(env.BaseEnv):
    def __init__(self, environ):
        super(Environment, self).__init__()

        # Set the required variables from the wsgi environ object
        for key, value in environ.iteritems():
            key = key.replace('.', '_')
            if key in self:
                self[key] = value

        # Fetch get/post variables from wsgi_input
        form = FS(fp=self.wsgi_input, environ=environ, keep_blank_values=1)

        # Replace the value (a morsel object) with it's actual value
        for key in form.keys():
            self.form[key] = form[key].value

        # Add additional variables provided by the base class
        super(Environment, self).extras()
