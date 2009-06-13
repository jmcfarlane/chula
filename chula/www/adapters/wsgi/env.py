"""
Manage the environment when python is using wsgi
"""

from cgi import FieldStorage

from chula.www.adapters import env

WSGI = 'WSGI'

class Environment(env.BaseEnv):
    def __init__(self, environ):
        super(Environment, self).__init__()
        
        # Indicate what type of adapter this is
        self.chula_adapter = WSGI

        # Set the required variables from the wsgi environ object
        self.fill(environ)

        # Check for redirects and recover the querystring
        if 'REDIRECT_QUERY_STRING' in environ:
            self.QUERY_STRING = environ.get('REDIRECT_QUERY_STRING')

        # Make sure REQUEST_URI is set
        if not 'REQUEST_URI' in environ:
            parts = []
            parts.append(environ.get('PATH_INFO', ''))
            self.REQUEST_URI = ''.join(parts)

        # Be nice to the Python wsiref simple_server
        if self.SERVER_SOFTWARE.startswith('WSGIServer/0.1 Python'):
            self.DOCUMENT_ROOT = None
            self.REMOTE_PORT = None
            self.SCRIPT_FILENAME = None
            self.SERVER_ADDR = None
            self.SERVER_ADMIN = None
            self.SERVER_SIGNATURE = None

        # Make sure SCRIPT_NAME is set
        if not self.SCRIPT_NAME:
            self.SCRIPT_NAME = self.PATH_INFO

        # Set http get or post variables
        self.form = FieldStorage(fp=self.wsgi_input,
                                 environ=environ,
                                 keep_blank_values=1)

        # Add additional variables provided by the base class
        super(Environment, self).extras()

    def __deepcopy__(self, memo={}):
        """
        Currently not all wsgi.foo objects are easy to deepcopy.  This
        method overloads BaseEnv to return a fresh object with wsgi
        input/error objects being "by reference" copies.
        """

        # Make a copy of the existing objects
        wsgi_errors = self.wsgi_errors
        wsgi_input = self.wsgi_input

        # Remove them from the collection
        self.remove('wsgi_errors')
        self.remove('wsgi_input')

        # Put them back (by reference)
        fresh = super(Environment, self).__deepcopy__(memo)
        fresh.wsgi_input = wsgi_input
        fresh.wsgi_errors = wsgi_errors

        return fresh
