# Python imports
import cgi
import os
import re
import sys
import traceback

# Project imports
from chula import collection, logger
from chula.www.controller import base
from chula.www import http

RE_STATIC_FILE = re.compile(r'.*\.(css|gif|jpg|js|png|txt|xsl|ico|json)$')

class Error(base.Controller):
    def _crappy_static_server(self, path):
        """
        Fetch a static file from disk, changing headers and HTTP
        status as appropriate.
        """

        if self.config.htdocs is None:
            raise NotImplementedError

        self.env.status = http.HTTP_OK
        if path.endswith('.css'):
            self.content_type = 'text/css'
        elif path.endswith('.js'):
            self.content_type = 'text/javascript'
        elif path.endswith('.gif'):
            self.content_type = 'image/gif'
        elif path.endswith('.jpg'):
            self.content_type = 'image/jpg'
        elif path.endswith('.xsl'):
            self.content_type = 'text/xsl'
        elif path.endswith('.json'):
            self.content_type = 'text/json'

        static = self.config.htdocs + path
        with open(static, 'r') as data:
            return data.read()

    def e404(self):
        request_uri = self.env.REQUEST_URI

        # Support standalone mode and serve static content ourselves
        if RE_STATIC_FILE.match(self.env.REQUEST_URI):
            try:
                return self._crappy_static_server(self.env.REQUEST_URI)
            except (NotImplementedError, IOError):
                pass

        # The url doesn't seem to be supported
        self.env.status = http.HTTP_NOT_FOUND

        return '<html><body><h1>404</h1></body></html>'

    def e500(self):
        log = logger.Logger().logger('chula.www.controller.error')

        exception = collection.Collection()
        try:
            context = self.model.exception
            exception.summary = context.exception
            exception.env = context.env
        except Exception, ex:
            print ex
            pass

        # Harvest additional context on the error
        try:
            etype, value, tb = sys.exc_info()
            error_context = traceback.format_tb(tb)
            error_msg = traceback.format_exception_only(etype, value)

            exception.traceback = error_context
            exception.message = error_msg
        except Exception, ex:
            print 'Exception:', ex

        # Hack:
        try:
            if exception.message[0].startswith('None'):
                exception.message = str(exception.summary)
        except Exception, ex:
            print ex
            pass

        # Log the error
        extra = {'clientip':self.env.REMOTE_ADDR}
        log.error(exception.summary, exc_info=(etype, value, tb), extra=extra)

        # Add the message to the view if debugging
        if not self.config.debug:
            return '<html><body><h1>500</h1></body></html>'

        # Expose the exception object to the model
        self.model.exception = exception

        return self.e500_render(self.model)

    def e500_render(self, model):
        exception = model.exception

        stack = ['<li>%s</li>' % cgi.escape(s) for s in exception.traceback]
        traceback_html = '<ol>%s</ol>' % ''.join(stack)

        template = """
        <html>
            <body>
                <h1>Application Error</h1>

                <h2>Summary</h2>
                %(summary)s

                <h2>Message</h2>
                %(message)s

                <h2>Traceback</h2>
                %(traceback)s
            </body>
        </html>
        """ % {
                'summary':cgi.escape(str(exception.summary), True),
                'message':cgi.escape(str(exception.message), True),
                'traceback':traceback_html,
              }

        return template
