"""
Chula helper module for working with web services
"""

import cPickle

from chula import error, json, collection, logger

class Transport(collection.RestrictedCollection):
    """
    Web service transport class designed to be subclassed to provide
    various means of encoding.
    """

    def __init__(self, controller):
        super(Transport, self).__init__()
        self.controller = controller
        self.log = logger.Logger(controller.config).logger('chula.webservice')

    def __privatekeys__(self):
        """
        Populate the private keys
        """

        return ('controller', 'log')

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

        :param kwargs: The collection of key=value arguments
        :type keyargs: Dict
        :param arg: The specific argument to be used
        :type arg: String
        :param default: The default value
        :type: default: Boolean

        The algorithm used is:
            1. Fetch from HTTP GET variables
            2. Fetch from HTTP POST variables
            3. Fetch from ``kwargs`` passed in the decorated method
            4. Use the default value set in the transport

        Currently supported keyword arguments:
            - x_header: Should the HTTP X-JSON header be used for payload
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

    def encode(self, **kwargs):
        """
        Each transport child class overloads this method to encode the
        supplied payload, into the appropriate transport encoding.
        For example when the transport is JSON, this method (defined
        in the subclass) will take the payload and :func:`json.dumps`
        it.
        """

        raise NotImplementedError('Subclasses must overload this method')

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
    of keyword arguments which are passed to the transport
    :meth:`chula.webservice.Transport.encode` method for use with
    making decisions.  This is best illustrated with a few examples:

    :param transport: Desired transpoort
    :type transport: :class:`str`, default is ``JSON``
    :param x_header: Should json payload use the HTTP X-JSON header
    :type x_header: :class:`bool`, default is ``False``
    :rtype: Decorator, see: :pep:`318`

    **Simple JSON web service method:**

    >>> from chula import webservice
    >>> from chula.www.controller import base
    >>>
    >>> class Webservice(base.Controller):
    ...     @webservice.expose()
    ...     def simple_json(self):
    ...         return {'some':'payload'}
    >>>

    ... Calling this webservice will look something like:

    >>> import json, urllib2
    >>> from chula.test.bat import PORT
    >>>
    >>> url = 'http://localhost:%s/webservice/simple_json' % PORT
    >>> payload = json.loads(urllib2.urlopen(url).read())
    >>> payload.keys()
    [u'msg', u'exception', u'data', u'success']
    >>> payload['success']
    True
    >>> payload['data']
    {u'some': u'payload'}

    ... You can also call this method with some GET args:

    >>> import json, urllib2
    >>> from chula.test.bat import PORT
    >>>
    >>> url = 'http://localhost:%s/webservice/simple_json?indent=2' % PORT
    >>> pretty_json = urllib2.urlopen(url).read()

    **A webservice that breaks, will always return valid payload:**

    >>> from chula import webservice
    >>> from chula.www.controller import base
    >>>
    >>> class Webservice(base.Controller):
    ...     @webservice.expose()
    ...     def broken(self):
    ...         return 0 / 0
    >>>

    ... Calling this webservice will look something like:

    >>> import json, urllib2
    >>> from chula.test.bat import PORT
    >>>
    >>> url = 'http://localhost:%s/webservice/broken' % PORT
    >>> payload = json.loads(urllib2.urlopen(url).read())
    >>> payload['success']
    False
    >>> payload['exception']
    u'integer division or modulo by zero'

    **JSON web service method that uses the X-JSON HTTP header:**

    >>> from chula import webservice
    >>> from chula.www.controller import base
    >>>
    >>> class Webservice(base.Controller):
    ...     @webservice.expose(x_header=True)
    ...     def xjson(self):
    ...         return {'some':'payload'}
    >>>

    ... Calling this webservice will look something like:

    >>> import json, urllib2
    >>> from chula.test.bat import PORT
    >>>
    >>> url = 'http://localhost:%s/webservice/xjson' % PORT
    >>> payload = json.loads(urllib2.urlopen(url).info().get('X-JSON'))
    >>> payload.keys()
    [u'msg', u'exception', u'data', u'success']
    >>> payload['success']
    True
    >>> payload['data']
    {u'some': u'payload'}

    **PICKLE web service method:**

    >>> from chula import webservice
    >>> from chula.www.controller import base
    >>>
    >>> class Webservice(base.Controller):
    ...     @webservice.expose(transport='PICKLE')
    ...     def pickle(self):
    ...         return {'some':'payload'}
    >>>

    ... Calling this webservice will look something like:

    >>> import cPickle, urllib2
    >>> from chula.test.bat import PORT
    >>>
    >>> url = 'http://localhost:%s/webservice/pickle' % PORT
    >>> payload = cPickle.loads(urllib2.urlopen(url).read())
    >>> payload.keys()
    ['msg', 'exception', 'data', 'success']
    >>> payload['success']
    True
    >>> payload['data']
    {'some': 'payload'}

    .. note::

       Using a :mod:`cPickle` transport will provide more "native"
       encoding.  This method maintains the non unicode encoded
       string.  Contrast this with the json transport which results in
       unicode encoded strings as a by product of json dumps/loads.

    .. note::

       It's also true that while :mod:`cPickle` is not portable to non
       Python clients, it's **way** faster, by orders of magnitude.

    **ASCII web service method:**

    >>> from chula import webservice
    >>> from chula.www.controller import base
    >>>
    >>> class Foo(base.Controller):
    ...     @webservice.expose(transport='ASCII')
    ...     def foo(self):
    ...         return {'some':'payload'}
    >>>

    This isn't super usefull, but say you the client is
    :program:`curl` or something, this might actually be easiser to
    work with.

    .. note::

       **Client's can also specify the transport they want:**

    >>> import json, urllib2
    >>> from chula.test.bat import PORT
    >>>
    >>> url = 'http://localhost:%s/webservice/pickle?transport=json' % PORT
    >>> payload = json.loads(urllib2.urlopen(url).read())
    >>> payload.keys()
    [u'msg', u'exception', u'data', u'success']

    Notice here that the webservice itself was configured to use the
    pickle transport, but the client specifically asked for json :)
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
                extra = {'clientip':ws.controller.env.REMOTE_ADDR}
                msg = 'Unhandled exception in webservice'
                ws.log.error(msg, exc_info=True, extra=extra)

            # Let the controller specify the msg if provided
            if hasattr(self, 'msg'):
                ws.msg = self.msg

            return ws.encode(**kwargs)
        return wrapper
    return decorator
