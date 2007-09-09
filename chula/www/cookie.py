"""
Cookie reads and writes cookies
"""

from mod_python import Cookie as Apache
import time
from chula import guid

class Cookie(object):
    def __init__(self, req, name='DEFAULT'):
        """
        @param req: Apache request object
        @type raq: mod_python.request
        """

        self.req = req
        self.HMAC = 'dg3683hdfd94ha2-kvd25zxzsrtyy'

        # Set the cookie name, setting the default value if needed
        if name == 'DEFAULT':
            self.name = 'tnk.cookie'
        else:
            self.name = name

        self.cookies = Apache.get_cookies(self.req,
                                          Apache.MarshalCookie,
                                          secret=self.HMAC)

        # Create the reqeuested cookie if it doesn't exist.  Usually this
        # will be a DEFAULT cookie, meaning it will be named whatever is
        # in the if condition above: if name == 'DEFAULT'
        if self.name not in self.cookies:
            self.persist(guid.guid())

    def exists(self):
        """
        Does the named cookie exist or not.
        @return: True/False
        """
        
        if self.cookies.has_key(self.name):
            return True
        else:
            return False
    
    def destroy(self):
        """
        Destroy cookie by saving the expire date to the past
        """
        
        c = Apache.MarshalCookie(self.name, '', self.HMAC)
        c.expires = time.time() - 60 * 1000
        c.path = '/' # /foo/bar would restrict the cookie to a directory
        Apache.add_cookie(self.req, c)

    def persist(self, value=None, path='/'):
        """
        Persist cookie to browser,
        @param value: Data to be saved in the cookie
        @type value: Dictionary, list, integer, string
        """
        if value is None:
            raise ValueError, "Please pass the value to be persisted"

        c = Apache.MarshalCookie(self.name, value, self.HMAC)
        c.expires = time.time() + 60 * 45
        c.path = path # /foo/bar would restrict the cookie to a directory
        Apache.add_cookie(self.req, c)
        self.cookies[self.name] = c

    def value(self):
        """
        Return the value of the named cookie.
        @return: Dictionary, list, integer, string
        """
        
        try:
            value = self.cookies[self.name].value
            return value
        except KeyError, ex:
            msg = 'Requested cookie does not exist: %s' % self.name
            raise KeyError, msg

