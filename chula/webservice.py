"""
Chula helper module for working with web services
"""

from chula import error, json, collection

class Transport(collection.RestrictedCollection):
    """
    Web service transport class designed to be subclassed to provide
    various means of encoding.
    """

    def __init__(self, env):
        super(Transport, self).__init__()
        self.env = env

    def __privatekeys__(self):
        """
        Populate the private keys
        """

        return ('env',)

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
        
        self.env.content_type = 'application/x-json'
        self.env.headers.append(('X-JSON', json.encode(self.strip())))

        return '<X-JSON Object>'

class ASCII(Transport):
    """
    Webservice that uses ascii as the transport layer
    """

    def encode(self):
        """
        Encode the transport into an acii string
        """
        
        self.env.content_type = 'text/plain'

        # With ascii we don't have any structure, so either return the
        # data or an exception if caught
        if not self.exception is None:
            return str(self.exception)
        else:
            return str(self.data)
