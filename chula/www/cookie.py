"""
Cookie reads and writes cookies
"""

from Cookie import SimpleCookie
from datetime import datetime
import pytz

from chula import data

class CookieCollection(SimpleCookie):
    def __init__(self, timeout=20, path='/', key=None):
        """
        Create a collection of cookies that share timeout and hash
        keys

        @param timeout: How long the cookie should live
        @type timeout: int (Unit of measure: minutes)
        """

        super(CookieCollection, self).__init__()
        self.timeout = timeout
        self.path = path
        self.key = key

    def headers(self):
        timeout = self.timeout * 60
        expires = data.date_add('m', timeout, datetime.now(pytz.utc))
        expires = expires.strftime('%a, %m-%b-%Y %H:%M:%S %Z')

        parts = []
        for key in self.keys():
            value = self.get(key).value
            parts.append('%s=%s;' % (key, value))

        parts.append('path=%s;' % self.path)
        parts.append('expires %s;' % expires)

        return ('Set-Cookie', ' '.join(parts))

    def destroy(self):
        self.timeout = -10
