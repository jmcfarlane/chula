"""
Generic base controller used by all web requests
"""

try:
    from mod_python import apache, util
except ImportError:
    import sys

    from chula.www import fakerequest as util

    print >> sys.stderr, "NOTICE: Unable to access mod_python"
    print >> sys.stderr, "NOTICE: Using chula.www.fakerequest.FakeRequest()"

from chula import collection, guid, error, session
from chula.www import cookie, env

class Controller(object):
    """
    The Controller class helps manage all web requests.  This is done
    by all requests being either of this class or a subclass.
    """

    def __init__(self, req, config):
        """
        Initialize the web request, performing taks common to all web
        requests.

        @param req: Apache request object
        @type req: req (mod_python request object)
        """
        
        self.content_type = 'text/html'
        self._load_http_vars(req)

        # TODO: Add specific object for GET vars as maybe != POST
        self.form = dict(self.req.form)
        self.env = env.Env(req)

        # Get user configuration
        self.config = config

        # Fetch the user's cookie
        self.cookie = cookie.Cookie(self.req,
                                    config.session_name,
                                    config.session_encryption_key,
                                    config.session_timeout)

        # Expose if the client supports cookies
        client_cookies_enabled = self.cookie.client_cookies_enabled
        self.env['chula_client_cookies_enabled'] = client_cookies_enabled

        # Start up session using the cookie's guid (or a fake one)
        if self.cookie.cookies is None: 
            self.session = session.Session(config, guid.guid())
        else:
            guid_ = self.cookie.value()
            self.session = session.Session(config, guid_)

        # Create a default model. This object is optionally populated by the
        # controller, or it can do it's own thing.
        self.model = collection.Collection()
        self.model.session = self.session
        self.model.env = self.env

    def _load_http_vars(self, req):
        """
        Takes the request object and fills self.* values based on it
        """

        self.req = req

        # If self.req.form exists and is of type util.FieldStorage trust
        # it's contents and move on, else set it (currently to the same
        # value that mod_python publisher would set it).
        try:
            if isinstance(self.req.form, util.FieldStorage):
                return
        except:
            self.req.form = util.FieldStorage(req, keep_blank_values=1)

    def _gc(self):
        """
        Complete garbage collection.  The intended purpose is to allow
        consolidated garbage collection specific to each project.
        This method gets called in the apache handler just before
        sending data to the browser.
        """

        pass

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
            self.req.headers_out['location'] = str(destination)
        except TypeError, ex:
            msg = 'Invalid redirection uri: %s, %s' % (destination, ex)
            raise error.ControllerRedirectionError(msg)

        if type == 'TEMPORARY':
            self.req.status = apache.HTTP_MOVED_TEMPORARILY
        elif type == 'PERMANENT':
            self.req.status = apache.HTTP_MOVED_PERMANENTLY
        else:
            msg = 'Unkonwn redirection type: %s' % type
            raise error.UnsupportedUsageError(msg)

        return 'REDIRECTING...'

