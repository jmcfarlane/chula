"""
Generic base controller used by all web requests.
"""

from chula import session
from chula.www import cookie

try:
    from mod_python import apache, util
except ImportError:
    from chula.www import fakerequest as util
    print "NOTICE: Unable to access mod_python"
    print "NOTICE: Creating FakeRequest object(s) and continuing anyway..."

class Controller(object):
    """
    The BaseController class helps manage all web requests.  This is done
    by all requests being either of this type, or of a descendant type.
    """

    def __init__(self, req, config):
        """
        Initialize the web request, performing taks common to all web
        requests.

        @param req: Apache request object
        @type req: req
        """
        
        self.content_type = 'text/html'
        self.load_http_vars(req)

        # Get user configuration
        self.config = config

        # Fetch the user's cookie
        ck = cookie.Cookie(self.req,
                           config.session_name,
                           config.session_encryption_key,
                           config.session_timeout)

        # Start up session using the cookie's guid
        guid = ck.value()
        self.session = session.Session(config, guid)

    def load_http_vars(self, req):
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
        except Exception:
            self.req.form = util.FieldStorage(req, keep_blank_values=1)

    def redirect(self, destination, type='TEMPORARY'):
        """
        Redirect the browser to another page.

        @param destination: URL of target destination
        @type destination: String
        """

        self.req.headers_out['location'] = destination

        if type == 'TEMPORARY':
            self.req.status = apache.HTTP_MOVED_TEMPORARILY
        elif type == 'PERMANENT':
            self.req.status = apache.HTTP_MOVED_PERMANENTLY
        else:
            raise ValueError, 'Unkonwn redirection type: %s' % type

        return 'REDIRECTING...'
