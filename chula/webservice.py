"""
Chula helper module for working with web services
"""

from chula import error, json, collection

class Transport(collection.RestrictedCollection):
    """
    Web service transport class designed to be subclassed to provide
    various means of encoding.
    """

    def __init__(self, req):
        super(Transport, self).__init__()
        self.req = req

    def __privatekeys__(self):
        """
        Populate the private keys
        """

        return ('req',)

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

class JSON(Transport):
    """
    Webservice that uses json as the transport layer
    """

    def encode(self):
        """
        Encode the transport into a json string and return X-JSON
        """

        self.req.content_type = 'application/x-json'
        self.req.headers_out.add('X-JSON', json.encode(self.strip()))

        return '<X-JSON Object>'
