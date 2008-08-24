"""
Chula adapter environment class
"""

from chula import error, collection

class BaseEnv(collection.RestrictedCollection):
    """
    Provide a consistent interface all adapters must conform to
    """

    @staticmethod
    def __validkeys__():
        """
        The minimum environment must at least adhere to the wsgi spec
        """

        return ('DOCUMENT_ROOT',
                'GATEWAY_INTERFACE',
                'HTTP_ACCEPT',
                'HTTP_ACCEPT_CHARSET',
                'HTTP_ACCEPT_ENCODING',
                'HTTP_ACCEPT_LANGUAGE',
                'HTTP_CONNECTION',
                'HTTP_COOKIE',
                'HTTP_HOST',
                'HTTP_KEEP_ALIVE',
                'HTTP_USER_AGENT',
                'PATH',
                'PATH_INFO',
                'QUERY_STRING',
                'REMOTE_ADDR',
                'REMOTE_HOST',
                'REMOTE_PORT',
                'REQUEST_METHOD',
                'REQUEST_URI',
                'SCRIPT_FILENAME',
                'SCRIPT_NAME',
                'SERVER_ADDR',
                'SERVER_ADMIN',
                'SERVER_NAME',
                'SERVER_PORT',
                'SERVER_PROTOCOL',
                'SERVER_SIGNATURE',
                'SERVER_SOFTWARE',
                'chula_class',
                'chula_method',
                'chula_module',
                'chula_package',
                'chula_version',
                'wsgi_errors',
                'wsgi_file_wrapper',
                'wsgi_input',
                'wsgi_multiprocess',
                'wsgi_multithread',
                'wsgi_run_once',
                'wsgi_url_scheme',
                'wsgi_version',
                'ajax_uri',
                'content_type',
                'cookies',
                'debug',
                'form',
                'headers',
                'route',
                'status',
               )

    def __defaults__(self):
        self.DOCUMENT_ROOT = collection.UNSET
        self.GATEWAY_INTERFACE = collection.UNSET
        self.HTTP_ACCEPT = collection.UNSET
        self.HTTP_ACCEPT_CHARSET = collection.UNSET
        self.HTTP_ACCEPT_ENCODING = collection.UNSET
        self.HTTP_ACCEPT_LANGUAGE = collection.UNSET
        self.HTTP_CONNECTION = collection.UNSET
        self.HTTP_COOKIE = collection.UNSET
        self.HTTP_HOST = collection.UNSET
        self.HTTP_KEEP_ALIVE = collection.UNSET
        self.HTTP_USER_AGENT = collection.UNSET
        self.PATH = collection.UNSET
        self.PATH_INFO = collection.UNSET
        self.QUERY_STRING = collection.UNSET
        self.REMOTE_ADDR = collection.UNSET
        self.REMOTE_HOST = collection.UNSET
        self.REMOTE_PORT = collection.UNSET
        self.REQUEST_METHOD = collection.UNSET
        self.REQUEST_URI = collection.UNSET
        self.SCRIPT_FILENAME = collection.UNSET
        self.SCRIPT_NAME = collection.UNSET
        self.SERVER_ADDR = collection.UNSET
        self.SERVER_ADMIN = collection.UNSET
        self.SERVER_NAME = collection.UNSET
        self.SERVER_PORT = collection.UNSET
        self.SERVER_PROTOCOL = collection.UNSET
        self.SERVER_SIGNATURE = collection.UNSET
        self.SERVER_SOFTWARE = collection.UNSET
        self.chula_class = collection.UNSET
        self.chula_method = collection.UNSET
        self.chula_module = collection.UNSET
        self.chula_package = collection.UNSET
        self.chula_version = collection.UNSET
        self.route = collection.UNSET
        self.wsgi_errors = None
        self.wsgi_file_wrapper = None
        self.wsgi_input = None
        self.wsgi_multiprocess = None
        self.wsgi_multithread = None
        self.wsgi_run_once = None
        self.wsgi_url_scheme = None
        self.wsgi_version = None
        self.ajax_uri = collection.UNSET
        self.content_type = 'text/plain'
        self.cookies = None
        self.debug = True
        self.headers = []
        self.form = {}
        self.status = 200

