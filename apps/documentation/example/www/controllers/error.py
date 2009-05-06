"""
Controller to properly handle error conditions
"""

from __future__ import with_statement
import re

from chula.www import http

from example.www.controllers import base

RE_STATIC_FILE = re.compile(r'.*\.(css|gif|jpg|js|png|txt)$')

class Error(base.Base):
    def __init__(self, env, config):
        """
        All error methods start off with an HTTP 500
        """

        super(Error, self).__init__(env, config)
        self.env.status = http.HTTP_INTERNAL_SERVER_ERROR

    def _crappy_static_server(self, path):
        """
        Fetch a static file from disk, changing headers and HTTP
        status as appropriate.
        """

        self.env.status = http.HTTP_OK
        if path.endswith('.css'):
            self.content_type = 'text/css'
        elif path.endswith('.gif'):
            self.content_type = 'image/gif'
        elif path.endswith('.jpg'):
            self.content_type = 'image/jpg'

        static = self.config.local.root + '/www' + path
        with open(static, 'r') as data:
            return data.read()

    def e404(self):
        """
        Serve static content, as well as handle 404 requests
        """

        request_uri = self.env.REQUEST_URI

        # Support standalone mode and serve static content ourselves
        if not RE_STATIC_FILE.match(self.env.REQUEST_URI) is None:
            try:
                return self._crappy_static_server(self.env.REQUEST_URI)
            except IOError:
                raise

        # The url doesn't seem to be supported
        self.env.status = http.HTTP_NOT_FOUND

        view = self.template('/error/e404.tmpl')
        return view.render(model=self.model)
    
    def e500(self):
        view = self.template('/error/e500.tmpl')
        return view.render(model=self.model)
