"""
Chula helper module for working with web services
"""

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

    def __fetch_arg__(self, kwargs, arg, default):
        """
        Fetch a keyword argument from the passed list.

        @param kwargs: The collection of key=value arguments
        @type key: Dict
        @param arg: The specific argument to be used
        @type arg: String
        @param default: The default value
        @type: arg: Boolean
        
        The algorithm used is:
            1. Fetch from HTTP GET variables
            2. Fetch from HTTP POST variables
            3. Fetch from **kwargs passed in the decorated method
            4. Use the default value set in the transport

        Currently supported keyword arguments:
            - x_header: Should the HTTP X-JSON header be used for payload

        """

        return self.controller.form.get(arg, kwargs.get(arg, default))

class JSON(Transport):
    """
    Webservice that uses json as the transport layer
    """

    def encode(self, **kwargs):
        """
        Encode the transport into a json string and return X-JSON
        """

        if self.__fetch_arg__(kwargs, 'x_header', True):
            self.controller.content_type = 'application/x-json'
            self.controller.env.headers.append(('X-JSON',
                                                json.encode(self.strip())))

            return '<X-JSON Object>'
        else:
            self.controller.content_type = 'text/plain'
            return json.encode(self.strip())

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

def expose(**kwargs):
    """
    Decorator for exposing a method as a web service.  It takes a list
    of keyword arguments which are passed to the webservice encoding()
    method for use with making decisions.  For example:
    @webservice.handler(x_header=False) will cause services using JSON
    as a transport to include the payload in the actual body, rather
    than using the X-JSON HTTP header.  You can also set these via
    HTTP GET arguments. See chula.webservice.Transport.__fetch_arg__()
    for more information.
    """

    def decorator(fcn): 
        def wrapper(self):
            transport = self.form.get('transport').upper()
            ws = getattr(Transports, transport, JSON)(self)

            try:
                ws.data = fcn(self)
                ws.success = True
            except Exception, ex:
                ws.exception = str(ex)

            return ws.encode(**kwargs)
        return wrapper
    return decorator
