"""
Cookie reads and writes cookies
"""

from Cookie import SimpleCookie
from datetime import datetime
import pytz

from chula import data

class CookieCollection(SimpleCookie):
    def __init__(self, timeout=20, path='/', input=None):
        """
        Create a collection of cookies

        @param timeout: How long the cookie should live
        @type timeout: int (Unit of measure: minutes)
        """

        super(CookieCollection, self).__init__(input)
        self.timeout = timeout
        self.path = path
        self.domain = None

    def headers(self):
        timeout = self.timeout * 60
        now = datetime.now(pytz.timezone('GMT'))
        expires = data.date_add('s', timeout, now)
        expires = expires.strftime('%a, %d-%b-%Y %H:%M:%S %Z')

        cookies = []
        for key, cookie in self.iteritems():
            # Don't write out cookies that are prefixed with underbars
            # as they are considered private. This also has the side
            # effect of not writing out Urchin cookies like crazy :)
            if not key.startswith('_'):
                header = []
                header.append('%s=%s' % (key, cookie.value))
                header.append('expires=%s' % expires)
                header.append('path=%s' % self.path)
                header.append('domain=%s' % self.domain)
                cookies.append(('Set-Cookie', '; '.join(header)))

        return cookies

    def destroy(self):
        self.timeout = -10000
        #self['expired'] = True
