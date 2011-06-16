"""
Chula configuration class (restricted collection class)
"""

# Python imports
import logging

# Project imports
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
                'auto_reload',
                'classpath',
                'construction_controller',
                'construction_trigger',
                'debug',
                'error_controller',
                'htdocs',
                'local',
                'log',
                'log_level',
                'mapper',
                'mqueue_db',
                'mqueue_host',
                'mqueue_port',
                'session',
                'session_db',
                'session_encryption_key',
                'session_host',
                'session_max_stale_count',
                'session_memcache',
                'session_name',
                'session_nosql',
                'session_password',
                'session_port',
                'session_timeout',
                'session_username',
                'strict_method_resolution',
                )

    def __defaults__(self):
        self.add_timer = True
        self.auto_reload = False
        self.classpath = collection.UNSET
        self.construction_controller = None
        self.construction_trigger = None
        self.debug = True
        self.error_controller = ''
        self.htdocs = None
        self.local = collection.Collection()
        self.log = '/tmp/chula.log'
        self.log_level = logging.WARNING
        self.mapper = 'ClassPathMapper'
        self.mqueue_db = '/tmp/chula/mqueue'
        self.mqueue_host = 'localhost'
        self.mqueue_port = 8001
        self.session_db = 'chula_session'
        self.session_encryption_key = 'chula-session-key'
        self.session_host = 'localhost'
        self.session_max_stale_count = 10
        self.session_memcache = [('localhost:11211', 1)]
        self.session_name = 'chula-session'
        self.session_nosql = None
        self.session_password = 'chula'
        self.session_port = 5432
        self.session_timeout = 30
        self.session = True
        self.session_username = 'chula'
        self.strict_method_resolution = False

