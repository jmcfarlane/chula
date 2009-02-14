"""
Chula base adapter for all supported web adapters
"""

from copy import deepcopy
import re
import time

import chula
from chula import collection, error, guid
from chula.www import cookie
from chula.www.mapper.standard import StandardMapper

RE_HTML = re.compile(r"</body>\s*</html>\s*$", re.IGNORECASE)

class BaseAdapter(object):
    def __init__(self, config):
        self.config = config
        self.timer_start()

        self.controller = None
        self.mapper = None

    def execute(self):
        self.controller = self.fetch_controller()

        # Call the controller method and if an exception is raised,
        # use the configured e500 controller.  If that breaks, it's up
        # to your web server custom 500 handler to handle things.
        try:
            html = self.controller.execute()
        except Exception, ex:
            # Prepare a collection to hold exception context
            context = collection.Collection()
            context.exception = ex
            context.env = deepcopy(self.controller.env)
            context.form = deepcopy(self.controller.form)

            # Try the error controller (and set an exception
            # attribute in the model)
            self.controller = self.mapper.map(500)
            self.controller.model.exception = context

            # Don't yield yet, need to replace to add chula stuff
            html = self.controller.execute()

        # Write the returned html to the request object.
        # We're manually casting the view as a string because Cheetah
        # templates seem to require it.  If you're not using Cheetah,
        # sorry... str() is cheap  :)
        if not html is None:
            html = str(html)
            written = False

            # Add info about server info and processing time
            if self.config.add_timer:
                timer = """
                    <div style="display:none;">
                        <div id="CHULA_ADAPTER">%s</div>
                        <div id="CHULA_SERVER">%s</div>
                        <div id="CHULA_VERSION">%s</div>
                        <div id="CHULA_COST">%f ms</div>
                    </div></body></html>
                    """ % (self.controller.env.chula_adapter,
                           self.controller.env.server_hostname,
                           self.controller.env.chula_version,
                           (time.time() - self.timer) * 1000)

                yield RE_HTML.sub(timer, html)
                written = True

            if not written:
                yield html
        else:
            raise error.ControllerMethodReturnError()

        # Add the content type to the environment
        self.env.content_type = self.controller.content_type

        # Add the cookies to the headers
        self.env.headers.extend(self.env.cookies.headers())

        # If this is an under construction page do not try to persist
        # session, avoid as many dependencies as possible
        if self.env.under_construction:
            self.env.status = 503
        else:
            # Persist session and perform garbage collection
            try:
                self.controller._pre_session_persist()
                self.controller.session.persist()
            except error.SessionUnableToPersistError():
                # Need to assign an error controller method to call here
                raise
            except Exception:
                # This is a downstream exception, let them handle it
                raise
            finally:
                self.controller._gc()

    def timer_start(self):
        if self.config.add_timer:
            self.timer = time.time()
        else:
            self.timer = None

    def set_environment(self, env):
        self.env = env
        self.env.headers = []

        # Initialize cookies
        self.env.cookies = cookie.CookieCollection()
        self.env.cookies.timeout = self.config.session_timeout
        self.env.cookies.key = self.config.session_encryption_key
        self.env.cookies.domain = self.env.HTTP_HOST

        # Make sure the domain gets set
        if self.env.cookies.domain is None:
            self.env.cookies.domain = self.env.SERVER_NAME

        # Load exising cookies sent from the client (browser)
        if not self.env.HTTP_COOKIE is None:
            self.env.cookies.load(self.env.HTTP_COOKIE)

    def add_header(self, header):
        self.env.headers.append(header)

    def fetch_controller(self):
        self.mapper = StandardMapper(self.config, self.env)

        # Load the controller, using e404 if not found
        try:
            controller = self.mapper.map()
        except error.ControllerClassNotFoundError:
            controller = self.mapper.map(404)

        controller.env.route = self.mapper.route

        return controller
