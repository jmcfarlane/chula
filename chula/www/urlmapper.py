"""
Base class to convert HTTP url path into a Python object path.  This
class can be subclassed to customize the url mapping behavior.
"""

import copy
import re

from chula import collection, error

DEFAULT_MODULE = 'home'
DEFAULT_METHOD = 'index'

class UrlMapper(object):
    def __init__(self, config, uri):
        # Check to make sure the config is available
        if config.classpath is None:
            msg = ('[cfg.classpath] must be specified in your configuration.'
                   ' See documentation for help on how to set this.')
            raise error.UnsupportedConfigError(msg)
            
        self.config = config
        self.uri = uri

        # Set the default route values
        self.route = collection.Collection()
        self.route.package = self.config.classpath
        self.route.module = DEFAULT_MODULE
        self.route.method = DEFAULT_METHOD

        # Set the default [404] route values
        self.route_404 = copy.copy(self.route)
        self.route_404.module = self.config.error_controller
        self.route_404.method = 'e404'

    def default_route(self):
        """
        Create the default route which will [later] map to a Python
        object.  The default route is either the homepage, or a 404
        page.
        """

        if self.uri != '/' and not self.uri.startswith('/?'):
            self.route = copy.copy(self.route_404)

    def parse(self):
        """
        Update the route by passing the url thru the mapper (regex)
        TODO: Add support for packages
        """

        parts = re.match(self.mapper(), self.uri)
        if not parts is None:
            for key, value in parts.groupdict().iteritems():
                if not value is None:
                    self.route[key] = value

    def import_module(self):
        path = '%s.%s' %  (self.config.classpath, self.route.module)
        class_name = self.route.module.capitalize()
        self.route.class_name = class_name
        try:
            module = __import__(path, globals(), locals(), [class_name])
        except ImportError, ex:
            # Reconstruct the route from the route_error we
            # made earlier, and let its e404 method handle things
            if not self.config.debug:
                self.route = self.route_404
                module = self.import_module()
            else:
                msg = '%s - %s' % (path, ex)
                raise error.ControllerModuleNotFoundError(msg)

        except Exception:
            raise

        return module
            

    def map(self):
        """
        Return a reference to the controller module?
        """

        self.default_route()
        self.parse()

        # Import the controller module
        module = self.import_module()

        # Instantiate the controller class from the module
        controller = getattr(module, self.route.class_name, None)

        if controller is None:
            msg = '%(module)s.%(class_name)s' % self.route
            raise error.ControllerClassNotFoundError(msg)
        
        self.controller = controller
        return controller

    def bind(self):
        # Make sure we don't try to load a private method
        if self.route.method.startswith('_'):
            self.route.method = DEFAULT_METHOD

        # Lookup the requested method to make sure it exists
        method = getattr(self.controller, self.route.method, None)

        # Fallback on the default method if the requested does not exist
        if not self.config.strict_method_resolution and method is None:
            method = getattr(self.controller, DEFAULT_METHOD, None)

        # If we still don't have a method something is very wrong
        if method is None:
            msg = '%(class_name)s.%(method)s()' % self.route
            raise error.ControllerMethodNotFoundError(msg)

        self.controller.execute = method
        self.update_env()
    
    def mapper(self):
        """
        The mapper is the regular expression responsible for how the
        url is actually mapped.
        """
        
        return (r'^/'
                r'(?P<module>[a-zA-Z]+[_a-zA-Z0-9]*)/'
                r'((?P<method>[a-zA-Z]+[_a-zA-Z0-9]*)/)?'
                r'((\?(?P<args>.*))?)?$')


    def update_env(self):
        #env = self.controller.env
        #env['chula_class'] = route.class_name
        #env['chula_method'] = route.method
        #env['chula_module'] = route.module
        #env['chula_version'] = chula.version

        return
