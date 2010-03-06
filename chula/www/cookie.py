"""
Cookie reads and writes cookies
"""

from Cookie import SimpleCookie
from datetime import datetime

from chula import data

class CookieCollection(SimpleCookie):
    def __init__(self, config=None, timeout=20, path='/', input=None):
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
        now = datetime.utcnow()
        expires = data.date_add('s', timeout, now)
        expires = expires.strftime('%a, %d-%b-%Y %H:%M:%S %Z')

        cookies = []
        for key, cookie in self.iteritems():
            # Don't write out cookies that are prefixed with underbars
            # as they are considered private. This also has the side
            # effect of not writing out Urchin cookies like crazy :)
            if key.startswith('_'):
                # TODO: find a better way to avoid writing Urchin cookies
                continue

            if not self.domain is None:
                # Domain must be prefixed with "." and exclude the
                # port.  If the domain already has a "." prefix we've
                # already seen this domain name and can skip.
                # REFERENCE: RFC 2109, RFC 2965
                if not self.domain.startswith('.'):
                    self.domain = '.' + self.domain.split(':')[0]

                # If the domain doesn't look to be a real FQDN, remove:
                if not self.domain.count('.') > 1:
                    self.domain = None

            # Always include the name of the cookie first
            header = []
            header.append('%s=%s' % (key, cookie.value))

            # Supported cookie attributes
            header.append('Expires=%s' % expires)
            header.append('Path=%s' % self.path)

            # Don't include the domain for sites that only use hostnames
            # eg: http://wiki/foo/bar/file.html
            if not self.domain is None:
                header.append('Domain=%s' % self.domain)

            # Create the full header tuple
            cookies.append(('Set-Cookie', '; '.join(header)))

        return cookies

    def destroy(self):
        self.timeout = -10000
