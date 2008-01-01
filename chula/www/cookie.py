"""
Cookie reads and writes cookies
"""

import time

from mod_python import Cookie as Apache

from chula import guid

class Cookie(object):
    def __init__(self, req, name, encryption_key, timeout):
        """
        Create a cookie object

        @param req: Apache request object
        @type req: mod_python.request
        """

        self.req = req
        self.name = name
        self.HMAC = encryption_key
        self.timeout = timeout
        self.client_cookies_enabled = False

        # Fetch the cookie from the client
        try:
            self.cookies = Apache.get_cookies(self.req,
                                              Apache.MarshalCookie,
                                              secret=self.HMAC)
        except TypeError, ex:
            # ^-- Defect near line 347 in mod_python-3.3.1's Cookie.py
            self.cookies = None

        # Determine if cookies are supported by the client, and persist
        if not self.cookies is None:
            # Determine support (exposed by chula.www.controller)
            if len(self.cookies) > 0:
                self.client_cookies_enabled = True

            # Persist session
            if self.name not in self.cookies:
                self.persist(guid.guid())
            else:
                self.persist(self.value())
        else:
            pass #TODO: Probably need to log this somehow

    def exists(self):
        """
        Does the named cookie exist or not.

        @return: bool
        """
        
        if self.name in self.cookies:
            return True
        else:
            return False
    
    def destroy(self):
        """
        Destroy cookie by saving the expire date to the past

        TODO: Refactor this into persist()
        """
        
        c = Apache.MarshalCookie(self.name, '', self.HMAC)
        c.expires = time.time() - 60 * 1000
        c.path = '/' # /foo/bar would restrict the cookie to a directory
        Apache.add_cookie(self.req, c)

    def persist(self, value=None, path='/'):
        """
        Persist cookie to browser

        @param value: Data to be saved in the cookie
        @type value: dict, list, int, str
        """

        if value is None:
            raise ValueError, "Please pass the value to be persisted"

        c = Apache.MarshalCookie(self.name, value, self.HMAC)
        if self.timeout > 0:
            c.expires = time.time() + 60 * self.timeout

        c.path = path # /foo/bar would restrict the cookie to a directory
        Apache.add_cookie(self.req, c)

        # Add the new cookie to the list [if possible]
        if not self.cookies is None:
            self.cookies[self.name] = c

    def value(self):
        """
        Return the value of the named cookie

        @return: Dictionary, list, integer, string
        """
        
        try:
            value = self.cookies[self.name].value
            return value
        except (KeyError, TypeError):
            msg = 'Requested cookie does not exist: %s' % self.name
            raise KeyError(msg)

