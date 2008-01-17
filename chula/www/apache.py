"""
Chula apache handler
"""

import copy
import time
import re

from mod_python import apache as APACHE

import chula
from chula import error

def _handler(req, config):
    if config.add_timer:
        TIME_start = time.time()
    DEFAULT_METHOD = 'index'
    regexp = (r'^/'
              r'(?P<module>[a-zA-Z]+[_a-zA-Z0-9]*)/'
              r'((?P<method>[a-zA-Z]+[_a-zA-Z0-9]*)/)?'
              r'((\?(?P<args>.*))?)?$')

    # Create the default route which will [later] map to a Python object
    if req.unparsed_uri == '/' or req.unparsed_uri.startswith('/?'):
        route = {'module':'home', 'method':DEFAULT_METHOD}
    else:
        # Consider the page a 404 until proven otherwise
        route_404 = {'module':config.error_controller, 'method':'e404'}
        route = copy.copy(route_404)

    # Update any parts we should use based on the url
    parts = re.match(regexp, req.unparsed_uri)
    if not parts is None:
        for key, value in parts.groupdict().iteritems():
            if not value is None:
                route[key] = value

    # The first letter of a class is always uppercase (PEP8)
    route['class'] = route['module'].capitalize()

    # Check to make sure the config is available
    if config.classpath is None:
        msg = ('[cfg.classpath] must be specified in your apache handler. '
               'See documentation for help on how to set this.')
        raise error.UnsupportedConfigError(msg)

    # Import the controller module
    try:
        module =  __import__(config.classpath + '.' + route['module'],
                             globals(), locals(), [route['class']])
    except ImportError, ex:
        # Debugging info, toggle for use
        if False:
            req.content_type = 'text/html'
            req.write(str(route))
            return APACHE.OK

        # If debugging raise an exception, else reconstruct the error
        # controller from the copy.copy() we made earlier, and let the
        # e404 method handle things
        if not config.debug:
            route = route_404
            route['class'] = route['module'].capitalize()
            module =  __import__(config.classpath + '.' + route['module'],
                                 globals(), locals(), [route['class']])
        else:
            msg = config.classpath + '.' + route['module'] + ' - ' + str(ex)
            raise error.ControllerModuleNotFoundError(msg)

    except Exception:
        raise

    # Instantiate the controller class from the module
    controller = getattr(module, route['class'], None)
    if controller is None:
        msg = '%s.%s' % (route['module'], route['class'])
        raise error.ControllerClassNotFoundError(msg)

    controller = controller(req, config)

    # Set the Apache content type (specified by the controller)
    req.content_type = controller.content_type

    # Make sure we don't try to load a private method
    if route['method'].startswith('_'):
        route['method'] = DEFAULT_METHOD

    # Lookup the requested method to make sure it exists
    method = getattr(controller, route['method'], None)

    # Fallback on the default method if the requested does not exist
    if not config.strict_method_resolution and method is None:
        method = getattr(controller, DEFAULT_METHOD, None)

    # If we still don't have a method something is very wrong
    if method is None:
        msg = '%s.%s()' % (route['class'], route['method'])
        raise error.ControllerMethodNotFoundError(msg)

    # Expose Chula specific environment information
    controller.env['chula_version'] = chula.version
    controller.env['chula_module'] = route['module']
    controller.env['chula_class'] = route['class']
    controller.env['chula_method'] = route['method']

    # Call the controller method
    html = method()

    # Persist session and perform garbage collection
    try:
        controller._pre_session_persist()
        controller.session.persist()
    except error.SessionUnableToPersistError():
        # Need to assign an error controller method to call here
        raise
    except Exception:
        # This is a downstream exception, let them handle it
        raise
    finally:
        controller._gc()

    # Write the returned html to the request object.
    # We're manually casting the view as a string because Cheetah
    # templates seem to require it.  If you're not using Cheetah,
    # sorry... str() is cheap  :)
    if not html is None:
        html = str(html)

        # Add info about server info and processing time
        written = False
        if config.add_timer:
            end = html[-8:].strip()
            for node in ('</html>', '</HTML>'):
                if end == node:
                    cost = (time.time() - TIME_start) * 1000
                    req.write(html.replace(node, """
                        <div style="display:none;">
                            <div id="CHULA_SERVER">%s</div>
                            <div id="CHULA_COST">%f ms</div>
                        </div>
                        """ % (controller.env['server_hostname'],
                               cost)))
                    req.write(node)
                    written = True
                    break

        if not written:
            req.write(html)
    else:
        raise error.ControllerMethodReturnError()


    # If we got here, all is well
    return APACHE.OK

def handler(fcn):
    def wrapper(req):
        config = fcn()
        return _handler(req, config)

    return wrapper

