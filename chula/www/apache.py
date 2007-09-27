"""
Chula apache handler
"""

from mod_python import apache as APACHE

from chula import error, config as CONFIG

def _handler(req, config):
    # The controller is the first word after the host:port
    # Here uri will hold search/results where the first part is used to
    # derive the module and class, the second is used to dervie the method
    # to call.
    uri = req.unparsed_uri.split('/')[1:]
    suffix = ''

    # Determine if this is the homepage or not
    if len(uri) > 1:
        controller_name = uri[0] + suffix
        class_name = uri[0][0].upper() + uri[0][1:] + suffix
        method_name = uri[1].split("?")[0]  # Remove ? from method name

        # If there is no action requested, then assume the default method is 
        # being called
        if method_name == "":
            method_name = "index"
        
    else:
        controller_name = 'home' + suffix
        class_name = 'Home' + suffix
        method_name = 'index'

    # Import the controller module
    if config.classpath == CONFIG.Config.UNSET:
        msg = ('[cfg.classpath] must be specified in your apache handler. '
               'See documentation for help on how to set this.')
        raise error.UnsupportedConfigError(msg)

    classpath = '%s.' % config.classpath
    module =  __import__(classpath + controller_name,
                         globals(),
                         locals(),
                         [class_name])

    # Instantiate the controller class from the module
    controller = getattr(module, class_name, None)
    if controller is None:
        msg = """
        The %s module needs to have a class named %s!
        """ % (controller_name, class_name)
        raise NameError, msg

    controller = controller(req, config)

    # Set the Apache content type
    req.content_type = controller.content_type

    # Lookup the requested method to make sure it exists
    method = getattr(controller, method_name, None)
    if method is None:
        msg = '%s.%s()' % (class_name, method_name)
        raise error.ControllerMethodNotFoundError(msg)

    # Execute the method and write the returned string to request object.
    # We're manually casting the return as a string because Cheetah
    # templates seem to require it.
    req.write(str(method()))

    # Persist session
    controller.session.persist()

    # If we got here, all is well
    return APACHE.OK

def handler(fcn):
    def wrapper(req):
        config = fcn()
        return _handler(req, config)

    return wrapper

