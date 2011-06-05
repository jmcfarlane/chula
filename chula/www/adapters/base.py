"""
Chula base adapter for all supported web adapters
"""

# Python imports
from copy import deepcopy
import os
import re
import sys
import time

# Project imports
from chula import collection, error, guid, logger
from chula.www import cookie
from chula.www.mapper import ClassPathMapper
from chula.www.mapper import RegexMapper

# Constants
EXTRA = {'clientip':''}
RE_HTML = re.compile(r'</body>\s*</html>\s*$', re.IGNORECASE)

# Cache namespace lookups
getmtime = os.path.getmtime

class BaseAdapter(object):
    def __init__(self, config):
        self.config = config
        self.timer_start()

        self.controller = None
        self.log = logger.Logger(config).logger('chula.www.adapters.base')
        self.mapper = None
        self._reload_all_modules()

    def _gc(self):
        del self.config
        del self.controller
        del self.env
        del self.mapper
        del self.timer

    def _reload_all_modules(self):
        if not self.config.auto_reload:
            return

        for k, v in sys.modules.items():
            mod = getattr(v, '__file__', None)

            if not mod:
                continue

            # After reloading mod will end with 'py', not 'pyc'.
            # Would like to understand this behavior, coding by
            # observation seems bad.
            if mod.endswith('.py'):
                mod += 'c'

            if not mod.endswith('.pyc'):
                self.log.debug('Skipping: %s' % mod, extra=EXTRA)
                continue

            try:
                stale = getmtime(mod[:-1]) > getmtime(mod)
            except:
                msg = 'Auto reload error while analyzing: %s' % k
                self.log.debug(msg, exc_info=True, extra=EXTRA)
                stale = False

            if stale:
                reload(v)
                self.log.debug('Auto reload successful: %s' % k)

    def exception(self, controller, ex):
        # Prepare a collection to hold exception context
        context = collection.Collection()
        context.exception = ex
        context.env = deepcopy(controller.env)
        context.form = deepcopy(controller.form)

        return context

    def execute(self):
        self.controller = self.fetch_controller()

        # Call the controller method and if an exception is raised,
        # use the configured e500 controller.  If that breaks, it's up
        # to your web server custom 500 handler to handle things.
        try:
            html = self.controller.execute()
        except Exception, ex:
            # Log the error
            extra = {'clientip':self.env.REMOTE_ADDR}
            msg = 'Unhandled exception in controller method'
            self.log.error(msg, exc_info=True, extra=extra)

            # Save off the exception before re-mapping the controller
            exception = self.exception(self.controller, ex)

            # Try the error controller (and set an exception
            # attribute in the model)
            self.controller = self.mapper.map(500)
            self.controller.model.exception = exception

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
                        <div id="CHULA_VERSION">%s</div>
                        <div id="CHULA_COST">%f ms</div>
                    </div></body></html>
                    """ % (self.controller.env.chula_adapter,
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
        for c in self.env.cookies.headers():
            self.log.debug('Added cookie: %s, %s' % c)

        # If this is an under construction page do not try to persist
        # session, avoid as many dependencies as possible
        if self.env.under_construction:
            self.env.status = 503
        elif self.config.session:
            # Persist session and perform garbage collection
            try:
                self.controller._pre_session_persist()
                self.controller.session.persist()
            except error.SessionUnableToPersistError:
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
        self.env.cookies = cookie.CookieCollection(config=self.config)
        self.env.cookies.domain = self.env.HTTP_HOST
        self.env.cookies.key = self.config.session_encryption_key
        self.env.cookies.timeout = self.config.session_timeout

        # Make sure the domain gets set
        if self.env.cookies.domain is None:
            self.env.cookies.domain = self.env.SERVER_NAME

        # Load exising cookies sent from the client (browser)
        if not self.env.HTTP_COOKIE is None:
            self.env.cookies.load(self.env.HTTP_COOKIE)

    def add_header(self, header):
        self.env.headers.append(header)

    def fetch_controller(self):
        mapper = self.config.mapper
        if mapper == 'ClassPathMapper':
            self.mapper = ClassPathMapper(self.config, self.env)
        elif isinstance(mapper, (tuple, frozenset, list, set)):
            self.mapper = RegexMapper(self.config, self.env, mapper)
        else:
            raise error.UnsupportedMapperError(mapper)

        # Load the controller, using e404 if not found
        try:
            controller = self.mapper.map()
        except error.ControllerImportError, ex:
            controller = self.mapper.map(500)
            controller.model.exception = self.exception(controller, ex)
        except error.ControllerClassNotFoundError:
            controller = self.mapper.map(404)

        controller.env.route = self.mapper.route

        return controller
