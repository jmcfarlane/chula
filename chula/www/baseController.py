"""
Generic base controller used by all web requests.  Each web project should
have a baseController that inherits from this.
"""

try:
    from mod_python import apache, util
except ImportError:
    from chula.www import fakerequest as util
    print "NOTICE: Unable to access mod_python"
    print "NOTICE: Creating FakeRequest object(s) and continuing anyway..."

from chula.session import Session
from chula.cookie import Cookie

class BaseController(object):
    """
    The BaseController class helps manage all web requests.  This is done
    by all requests being either of this type, or of a descendant type.
    """

    def __init__(self, req):
        """
        Initialize the web request, performing taks common to all web
        requests.

        @param req: Apache request object
        @type req: req
        """
        
        self.content_type = 'text/html'
        self.getRequest(req)

        # Get the user's cookie
        cookie = self.getCookie()

        # Expose user session (persisted by the apacheHandler)
        self.getSession(cookie.value())

    def getRequest(self, req):
        """
        Takes the request object and fills self.* values based on it
        """
        self.req = req

        # If self.req.form exists and is of type util.FieldStorage trust
        # it's contents and move on, else set it (currently to the same
        # value that mod_python publisher would set it).
        try:
            if isinstance(self.req.form, util.FieldStorage) is True:
                return
        except Exception:
            self.req.form = util.FieldStorage(req, keep_blank_values=1)

    def getSession(self, guid):
        """
        Get session data based on guid
        """
        self.userSession = Session(guid)
        self.session = self.userSession.values()

    def getCookie(self):
        """
        Pulls the cookie out of the request object
        """
        return Cookie(self.req, 'DEFAULT')

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
