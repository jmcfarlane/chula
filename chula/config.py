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

    @staticmethod
    def __validkeys__():
        """
        Initialize the supported configuration options with either a
        reasonable default, or I{UNSET}.
        """

        return ('add_timer',
                'classpath',
                'construction_controller',
                'construction_trigger',
                'debug',
                'error_controller',
                'local',
                'mqueue_db',
                'mqueue_host',
                'mqueue_poll',
                'mqueue_port',
                'session_db',
                'session_encryption_key',
                'session_host',
                'session_memcache',
                'session_name',
                'session_password',
                'session_port',
                'session_timeout',
                'session_username',
                'strict_method_resolution',
                )

    def __defaults__(self):
        self.add_timer = True
        self.classpath = collection.UNSET
        self.construction_controller = None
        self.construction_trigger = None
        self.debug = True
        self.error_controller = collection.UNSET
        self.local = collection.Collection()
        self.mqueue_db = '/tmp/chula/mqueue'
        self.mqueue_host = 'localhost'
        self.mqueue_poll = 5
        self.mqueue_port = 8001
        self.session_db = 'chula_session'
        self.session_encryption_key = collection.UNSET
        self.session_host = 'localhost'
        self.session_memcache = [('localhost:11211', 1)]
        self.session_name = 'chula-session'
        self.session_password = 'chula'
        self.session_port = 5432
        self.session_timeout = 30
        self.session_username = 'chula'
        self.strict_method_resolution = False

