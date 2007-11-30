"""
Chula apache handler
"""

import re

from mod_python import apache as APACHE

from chula import error

def _handler(req, config):
    DEFAULT_METHOD = 'index'
    regexp = (r'^/'
              r'(?P<module>[a-zA-Z]+[_a-zA-Z0-9]*)/'
              r'((?P<method>[a-zA-Z]+[_a-zA-Z0-9]*)/)?'
              r'((\?(?P<args>.*))?)?$')

    # Create the default route which will [later] map to a Python object
    if req.unparsed_uri == '/':
        route = {'module':'home', 'method':DEFAULT_METHOD}
    else:
        # Consider the page a 404 until proven otherwise
        route = {'module':config.error_controller, 'method':'e404'}

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
                             globals(),
                             locals(),
                             [route['class']])
    except ImportError, ex:
        # Debugging info, toggle for use
        if False:
            req.content_type = 'text/html'
            req.write(str(route))
            return APACHE.OK

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

    # Execute the method and write the returned string to request object.
    # We're manually casting the return as a string because Cheetah
    # templates seem to require it.
    output = method()
    if not output is None:
        req.write(str(output))
    else:
        raise error.ControllerMethodReturnError()

    # Persist session and perform garbage collection
    controller._pre_session_persist()
    controller.session.persist()
    controller._gc()

    # If we got here, all is well
    return APACHE.OK

def handler(fcn):
    def wrapper(req):
        config = fcn()
        return _handler(req, config)

    return wrapper

