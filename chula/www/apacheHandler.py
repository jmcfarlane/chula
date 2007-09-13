"""
Chula apache handler
"""

from mod_python import apache
from chula import config as CONFIG, chulaException

def handler(req, config):
    # The controller is the first word after the host:port
    # Here uri will hold search/results where the first part is used to
    # derive the module and class, the second is used to dervie the method
    # to call.
    uri = req.unparsed_uri.split('/')[1:]
    suffix = ''

    # Determine if this is the homepage or not
    if len(uri) > 1:
        controllerName = uri[0] + suffix
        className = uri[0][0].upper() + uri[0][1:] + suffix
        methodName = uri[1].split("?")[0]       # Remove ? from method name
        # If there is no action requested, then assume the default method is 
        # being called
        if methodName == "":
            methodName = "index"
        
    else:
        controllerName = 'home' + suffix
        className = 'Home' + suffix
        methodName = 'index'

    # Import the controller module
    if config.classpath == CONFIG.Config.UNSET:
        msg = ('[cfg.classpath] must be specified in your apacheHandler. '
               'See documentation for help on how to set this.')
        raise chulaException.UnsupportedConfigError(msg)

    classpath = '%s.' % config.classpath
    module =  __import__(classpath + controllerName,
                         globals(),
                         locals(),
                         [className])

    # Instantiate the controller class from the module
    controller = getattr(module, className, None)
    if controller is None:
        msg = """
        Come on... the %s module needs to have a class named %s!
        Clearly you deserve a good mocking.
        """ % (controllerName, className)
        raise NameError, msg

    controller = controller(req, config)

    # Set the Apache content type
    req.content_type = controller.content_type

    # Lookup the requested method to make sure it exists
    method = getattr(controller, methodName, None)
    if method is None:
        msg = 'Malformed URL: method does not exist: %s.%s()' % (className,
                                                                methodName)
        raise AttributeError, msg

    # Execute the method and write the returned string to request object.
    # We're manually casting the return as a string because Cheetah
    # templates seem to require it.
    req.write(str(method()))

    # Persist session
    controller.session.persist()

    # If we got here, all is well
    return apache.OK

def apacheHandler(fcn):
    def wrappedHandler(req):
        config = fcn()
        return handler(req, config)

    return wrappedHandler

