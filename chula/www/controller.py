"""
Generic base controller used by all web requests
"""

try:
    from mod_python import apache, util
except ImportError:
    from chula.www import fakerequest as util
    print "NOTICE: Unable to access mod_python"
    print "NOTICE: Creating FakeRequest object(s) and continuing anyway..."

from chula import chulaException, session
from chula.www import cookie

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
            msg = 'Unkonwn redirection type: %s' % type
            raise chulaException.UnsupportedUsageError(msg)

        return 'REDIRECTING...'

