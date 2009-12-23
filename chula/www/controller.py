"""
Generic base controller used by all web requests
"""

from chula import collection, guid, error, session
from chula.www import http

class Controller(object):
    """
    The Controller class helps manage all web requests.  This is done
    by all requests being either of this class or a subclass.
    """

    def __init__(self, env, config):
        """
        Initialize the web request, performing taks common to all web
        requests.

        @param env: Normalized environment (wsgi at a minimum)
        @type env: env WSGI environ object with a few extra objects
        """
        
        self.content_type = 'text/html'

        # Add some convenience attributes
        self.config = config
        self.env = env
        self.form = env.form

        # Create a default model. This object is optionally populated by the
        # controller, or it can do it's own thing.
        self.model = collection.Collection()
        self.model.env = self.env

        # Start up session using the cookie's guid (or a fake one)
        if self.config.session:
            if self.config.session_name in self.env.cookies:
                guid_ = self.env.cookies[self.config.session_name].value
            else:
                # Create a new guid create a cookie
                guid_ = guid.guid()
                self.env.cookies[self.config.session_name] = guid_

            # Instantiate session and expose to the model
            self.session = session.Session(self.config, guid_)
            self.model.session = self.session

    def _gc(self):
        """
        Complete garbage collection.  The intended purpose is to allow
        consolidated garbage collection specific to each project.
        This method gets called in the apache handler just before
        sending data to the browser.
        """

        self.session._gc()
        del self.config
        del self.env
        del self.form
        del self.model
        del self.session

    def _pre_session_persist(self):
        """
        Provide mechanism for removing items from session just prior
        to being persisted.  This is useful when you want to have
        unserializeable objects that need to be casted to a different
        type before being persisted to the database.  This usually
        means casting to a JSON encodable type.
        """

        pass

    def execute(self):
        """
        Provide a consistent method name for execution by the handler.
        This method is to be rebound by the UrlMapper.
        """

        return "ERROR: execute() has not been properly bound"

    def redirect(self, destination, type='TEMPORARY'):
        """
        Redirect the browser to another page.

        @param destination: URL of target destination
        @type destination: String
        """

        try:
            self.env.headers.append(('location', str(destination)))
        except TypeError, ex:
            msg = 'Invalid redirection content_type: %s, %s' % (destination, ex)
            raise error.ControllerRedirectionError(msg)

        if type == 'TEMPORARY':
            self.env.status = http.HTTP_MOVED_TEMPORARILY
        elif type == 'PERMANENT':
            self.env.status = http.HTTP_MOVED_PERMANENTLY
        else:
            msg = 'Unkonwn redirection type: %s' % type
            raise error.UnsupportedUsageError(msg)

        return 'REDIRECTING...'

