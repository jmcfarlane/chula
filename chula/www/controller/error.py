# Python2.5 backports
from __future__ import with_statement

# Python imports
import cgi
import mimetypes
import os
import re
import sys
import traceback

# Project imports
from chula import collection
from chula.www.controller import base
from chula.www import http

RE_STATIC_FILE = re.compile(r'.*\.([a-zA-Z0-9]+)$')

class Error(base.Controller):
    """Default error controller."""

    def _crappy_static_server(self, path):
        """
        Fetch a static file from disk, changing headers and HTTP
        status as appropriate.

        :param path: Path relative
        :type path: :attr:`chula.www.adapters.env.BaseEnv.REQUEST_URI`
        :rtype: :class:`str`
        """

        if self.config.htdocs is None:
            raise NotImplementedError

        self.env.status = http.HTTP_OK
        self.content_type = mimetypes.guess_type(path)[0]
        fq_path = self.config.htdocs + path

        # Attempt to serve the file only setting 200 OK if successful
        try:
            with open(fq_path, 'r') as data:
                return data.read()
        except Exception, ex:
            self.log.error(ex, extra={'clientip':self.env.REMOTE_ADDR})
            raise

    def e404(self):
        """
        Controller method to serve
        :attr:`chula.www.http.HTTP_NOT_FOUND` requests.
        """

        request_uri = self.env.REQUEST_URI

        # Support standalone mode and serve static content ourselves
        if RE_STATIC_FILE.match(self.env.REQUEST_URI):
            try:
                return self._crappy_static_server(self.env.REQUEST_URI)
            except (NotImplementedError, IOError):
                pass

        # The url doesn't seem to be supported
        self.env.status = http.HTTP_NOT_FOUND
        self.content_type = 'text/html'

        return self.e404_render()

    def e404_render(self):
        """
        Method to render the 404.  The intended use of this method is
        for an application to have an `error` controller that
        overloads this method.  This way applications can share the
        [somewhat crazy] logic of serving static resources (css, js),
        but still have a custom 404 page (if the web server isn't
        doing this).

        Here's an example error controller that might do this:

        >>> from chula.www.controller import error
        >>>
        >>> class Error(error.Error):
        ...     def e404_render(self):
        ...         return self.render('/view/e404.tmpl')
        >>>
        """

        return '<html><body><h1>404</h1></body></html>'

    def e500(self):
        """
        Controller method to serve
        :attr:`chula.www.http.HTTP_INTERNAL_SERVER_ERROR` requests.

        This method will add an ``exception`` key to the controller's
        ``self.model`` with the following attributes:

        .. attribute:: summary

           Summery information about the exception, of type :class:`str`

        .. attribute:: message

           Detailed description of the exception, of type :class:`str`

        .. attribute:: traceback

           Traceback, of type :class:`list`

        .. note::

           This method creates the above structure and then returns
           :meth:`e500_render`.  You should overload that method if
           you want to render the exception detail differently.
        """

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

        # Add the message to the view if debugging
        if not self.config.debug:
            return '<html><body><h1>500</h1></body></html>'

        # Expose the exception object to the model
        self.model.exception = exception

        return self.e500_render(self.model)

    def e500_render(self, model):
        """
        Method to render the :mod:`traceback` as html.  The intended
        use of this method is for an application to have an `error`
        controller that overloads this method.  This way applications
        can share the [somewhat crazy] logic of capturing a useful
        traceback, but render it uniquely to each application if it so
        desires.

        Here's an example error controller that might do this:

        >>> from chula.www.controller import error
        >>>
        >>> class Error(error.Error):
        ...     def e500_render(self):
        ...         return self.render('/view/error.tmpl')
        >>>

        Where the controller's :func:`render` method would use
        a Mako :class:`mako.template.Template` or something to render
        the model.

        With this type of implementation, the Mako template referenced
        above (:file:`webapp/view/error.tmpl`) might look like::

         % if not model.exception is None:
           <br/>
           <div class="exception">
             <fieldset>
               <legend>Application Error</legend>
               <h1>Summary</h1>
               ${model.exception['summary']}

               <h1>Message</h1>
               ${model.exception['message']}

               <h1>Traceback</h1>
               <ol>
                 % for part in model.exception['traceback']:
                   <li>${part | h}</li>
                 % endfor
               </ol>
             </fieldset>
           </div>
         % endif
        """

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
