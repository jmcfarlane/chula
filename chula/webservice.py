"""
Chula helper module for working with web services
"""

import cPickle

from chula import error, json, collection

class Transport(collection.RestrictedCollection):
    """
    Web service transport class designed to be subclassed to provide
    various means of encoding.
    """

    def __init__(self, controller):
        super(Transport, self).__init__()
        self.controller = controller

    def __privatekeys__(self):
        """
        Populate the private keys
        """

        return ('controller',)

    def __validkeys__(self):
        """
        Populate the supported keys
        """

        return ('data',
                'exception',
                'msg',
                'success')

    def __defaults__(self):
        """
        Set reasonable defaults
        """

        self.data = None
        self.exception = None
        self.msg = None
        self.success = False

    @staticmethod
    def __default__(controller, kwargs, arg, default):
        """
        Return a default value of the specified arg for use in the
        creation or calling of a webservice.  This method allows the
        webservice usage to be controlled either at creation or
        runtime (kwargs, http args).

        The algorithm used is:
            1. Fetch from HTTP GET variables
            2. Fetch from HTTP POST variables
            3. Fetch from **kwargs passed in the decorated method
            4. Use the default value set in the transport

        Currently supported keyword arguments:
            - x_header: Should the HTTP X-JSON header be used for payload

        @param kwargs: The collection of key=value arguments
        @type keyargs: Dict
        @param arg: The specific argument to be used
        @type arg: String
        @param default: The default value
        @type: default: Boolean
        """

        # The default then update with the desired algorithm
        retval = default

        # Use kwargs passed to the controller's decorator if available
        retval = kwargs.get(arg, retval)

        # Use HTTP POST if available
        retval = controller.env.form.get(arg, retval)

        # Use HTTP GET if available
        retval = controller.env.form_get.get(arg, retval)

        return retval

class JSON(Transport):
    """
    Webservice that uses json as the transport layer
    """

    def encode(self, **kwargs):
        """
        Encode the transport into a json string and return X-JSON
        """

        indent = self.__default__(self.controller, kwargs, 'indent', None)
        if indent:
            try:
                indent = int(indent)
            except:
                pass

        if self.__default__(self.controller, kwargs, 'x_header', False):
            self.controller.content_type = 'application/x-json'
            self.controller.env.headers.append(('X-JSON',
                                                json.encode(self.strip(),
                                                indent=indent)))

            return '<X-JSON Object>'
        else:
            self.controller.content_type = 'text/plain'
            return json.encode(self.strip(), indent=indent)

class PICKLE(Transport):
    """
    Webservice that uses Python pickling as the transport layer
    """

    def encode(self, **kwargs):
        """
        Encode the transport into a Python pickled string
        """
        
        self.controller.content_type = 'text/plain'
        return cPickle.dumps(dict(self.strip()))

class ASCII(Transport):
    """
    Webservice that uses ascii as the transport layer
    """

    def encode(self, **kwargs):
        """
        Encode the transport into an acii string
        """
        
        payload = str(self.data)
        self.controller.content_type = 'text/plain'

        # With ascii we don't have any structure, so either return the
        # data or an exception if caught
        if not self.exception is None:
            return str(self.exception)
        else:
            return payload

class Transports(object):
    """
    Bundle the transports in an object for use with getattr
    """

    JSON = JSON
    ASCII = ASCII
    PICKLE = PICKLE

def expose(**kwargs):
    """
    Decorator for exposing a method as a web service.  It takes a list
    of keyword arguments which are passed to the webservice encoding()
    method for use with making decisions.  For example:

        @webservice.expose(x_header=True)
        def foo(self):
            pass
    
    will cause services using JSON as a transport to include the
    payload in a X-JSON HTTP header rather than the actual body.  You
    can also set these via HTTP GET arguments. See
    chula.webservice.Transport.__default__() for more information.
    """

    def decorator(fcn): 
        def wrapper(self):
            transport = Transport.__default__(self,
                                              kwargs,
                                              'transport',
                                              'JSON').upper()

            # Reference the actual transport object, JSON is default
            webservice_callable = getattr(Transports, transport, None)
            if webservice_callable is None:
                raise error.WebserviceUnknownTransportError(transport)

            # Instantiate the web servie
            ws = webservice_callable(self)

            # Execute the controller and fill the webservice
            try:
                ws.data = fcn(self)
                ws.success = True
            except Exception, ex:
                ws.exception = str(ex)

            # Let the controller specify the msg if provided
            if hasattr(self, 'msg'):
                ws.msg = self.msg

            return ws.encode(**kwargs)
        return wrapper
    return decorator
