"""
Chula configuration class (restricted collection class)
"""

from chula import error, collection

class Config(collection.RestrictedCollection):
    """
    Chula configuration class.  This class provides an organized
    structure to hold all supported chula configuration options.  Most
    are optional, but a few are mandatory.  Any attribute with a
    default value of: I{UNSET} must be set by your configuration.
    Failure to do so will result in an exception.
    """

    def __validkeys__(self):
        """
        Initialize the supported configuration options with either a
        reasonable default, or I{UNSET}.
        """

        return ('add_timer',
                'classpath',
                'debug',
                'error_controller',
                'local',
                'session_db',
                'session_host',
                'session_port',
                'session_name',
                'session_memcache',
                'session_timeout',
                'session_encryption_key',
                'strict_method_resolution')

    def __defaults__(self):
        self.add_timer = True
        self.classpath = collection.UNSET
        self.debug = True
        self.error_controller = collection.UNSET
        self.local = collection.Collection()
        self.session_db = 'chula_session'
        self.session_host = 'localhost'
        self.session_port = 5432
        self.session_name = 'chula-session'
        self.session_memcache = [('localhost:11211', 1)]
        self.session_timeout = 30
        self.session_encryption_key = collection.UNSET
        self.strict_method_resolution = False

