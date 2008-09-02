"""
Chula adapter environment class
"""

import re

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
        self.HTTP_ACCEPT = None
        self.HTTP_ACCEPT_CHARSET = None
        self.HTTP_ACCEPT_ENCODING = None
        self.HTTP_ACCEPT_LANGUAGE = None
        self.HTTP_CONNECTION = None
        self.HTTP_COOKIE = None
        self.HTTP_HOST = None
        self.HTTP_KEEP_ALIVE = None
        self.HTTP_USER_AGENT = None
        self.PATH = collection.UNSET
        self.PATH_INFO = ''
        self.QUERY_STRING = ''
        self.REMOTE_ADDR = collection.UNSET
        self.REMOTE_HOST = collection.UNSET
        self.REMOTE_PORT = collection.UNSET
        self.REQUEST_METHOD = collection.UNSET
        self.REQUEST_URI = collection.UNSET
        self.SCRIPT_FILENAME = collection.UNSET
        self.SCRIPT_NAME = ''
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

    def _ajax_uri(self):
        protocol_type = re.match(r'(HTTPS?)', self.SERVER_PROTOCOL)
        if not protocol_type is None:
            protocol_type = protocol_type.group()
        else:
            msg = 'Unsupported protocol: %s' % self.SERVER_PROTOCOL
            raise ValueError(msg)

        return protocol_type.lower() + '://' + self.HTTP_HOST

    def _cookie(self):
        """
        Make sure HTTP_COOKIE exists even if empty
        """

        return self.get('HTTP_COOKIE', {})

    def extras(self):
        """
        Set extra environment variables, all being Chula specific
        """

        self.HTTP_COOKIE = self._cookie()
        self.ajax_uri = self._ajax_uri()
