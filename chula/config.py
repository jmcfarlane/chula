"""
Chula configuration class (restricted collection class)
"""

from chula import chulaException, collection

class Config(collection.Collection):
    """
    Chula configuration class.  This class provides an organized
    structure to hold all supported chula configuration options.  Most
    are optional, but a few are mandatory.  Any attribute with a
    default value of: I{UNSET} must be set by your configuration.
    Failure to do so will result in an exception.
    """

    UNSET = 'THIS ATTRIBUTE NEEDS TO BE SET BY YOU'
    supported = ['classpath',
                 'session_db',
                 'session_host',
                 'session_port',
                 'session_name',
                 'session_memcache',
                 'session_timeout',
                 'session_encryption_key',
                ]

    def __init__(self):
        """
        Initialize the supported configuration options with either a
        reasonable default, or I{UNSET}.
        """

        self.classpath = self.UNSET
        self.session_db = 'chula_session'
        self.session_host = 'localhost'
        self.session_port = 5432
        self.session_name = 'chula-session'
        self.session_memcache = [('localhost:11211', 1)]
        self.session_timeout = 30
        self.session_encryption_key = self.UNSET

    def __getitem__(self, key):
        """
        Allow restricted attribute access
        @param key: Key to be accessed
        @type key: String
        @return: Attribute
        """

        if key in self.supported:
            return self.get(key)
        else:
            raise chulaException.UnsupportedConfigError(append=key)

    def __setitem__(self, key, value):
        """
        Allow restricted attribute write access
        @param key: Key to be set
        @type key: String
        @param value: Value of key
        @type value: Anything
        """

        if key in self.supported:
            self.__dict__[key] = value
        else:
            raise chulaException.UnsupportedConfigError(append=key)

