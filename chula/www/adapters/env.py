"""
Chula adapter environment class (:pep:`0333`)
"""

from copy import deepcopy
import cgi
import re

from chula import error, collection
from chula.www import http

RE_HTTP_GET_OR_POST_KEY = re.compile(r'[:{}<>[\]]+')

class BaseEnv(collection.RestrictedCollection):
    """
    Provide a consistent interface all adapters must conform to
    """

    @staticmethod
    def __validkeys__():
        """
        The minimum environment must at least adhere to the wsgi spec
        """

        return ('CONTENT_LENGTH',
                'DOCUMENT_ROOT',
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
                'chula_adapter',
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
                'form_get',
                'form_post',
                'form_raw',
                'form_rest',
                'headers',
                'route',
                'status',
                'under_construction'
               )

    def __defaults__(self):
        """
        Set default values.  Values set to collection.UNSET must be
        set downstream, else we'll raise an exception.
        """

        self.CONTENT_LENGTH = 0
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
        self.REMOTE_HOST = None
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
        self.SERVER_SOFTWARE = 'Unknown WSGI provider'
        self.chula_adapter = collection.UNSET
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
        self.form = collection.UNSET
        self.form_get = collection.UNSET
        self.form_post = collection.UNSET
        self.form_raw = None
        self.form_rest = collection.UNSET
        self.status = http.HTTP_OK
        self.under_construction = False

    def __deepcopy__(self, memo={}):
        """
        Return a copy of a BaseEnv object
        """

        return self.copy_into(BaseEnv())

    def _ajax_uri(self):
        protocol_type = re.match(r'(HTTPS?)', self.SERVER_PROTOCOL)
        if not protocol_type is None:
            protocol_type = protocol_type.group()
        else:
            msg = 'Unsupported protocol: %s' % self.SERVER_PROTOCOL
            raise ValueError(msg)

        # Prefer HTTP_HOST over SERVER_NAME per PEP333
        domain = self.HTTP_HOST
        if domain is None:
            domain = self.SERVER_NAME

        return protocol_type.lower() + '://' + domain

    def _cookie(self):
        """
        Make sure HTTP_COOKIE exists even if empty
        """

        return self.get('HTTP_COOKIE', {})

    def _downcast_cgi_vars(self):
        """
        When mod_python.util.FieldStorage or cgi.FieldStorage
        encounter array types (think html checkboxes) it winds up
        being a Field() or MiniFieldStorage() object for mod_python or
        cgi respectively.  Both are intended to be accessed via a
        "value" attribute.  This method casts these objects so the
        actual value is held and thus can be referenced directly.  In
        the event the object doesn't have a "value" attribute it's
        left alone (not sure how this can happen, but it does).
        """

        if not self.form_raw is None:
            return

        for key in self.form.keys():
            if isinstance(self.form[key], list):
                for i in xrange(len(self.form[key])):
                    if not getattr(self.form[key][i], 'value', None) is None:
                        self.form[key][i] = self.form[key][i].value
                    else:
                        # Let me know if you can make this get called :)
                        pass

    def _clean_http_vars(self):
        """
        Analyze self.form and create/validate the following
        attributes:

         - self.form (holds POST + GET args with POST taking priority)
         - self.form_get (key/value pairs)
         - self.form_post (key/value pairs)
         - self.form_raw (usually xml or json)
        """

        # Cast any dict-like objects (FieldStorage for example) to
        # real dicts, so method like get() and iteritems() exist.
        try:
            self.form = dict(self.form)
        except TypeError:
            self.form = {}

        # Create object to hold only HTTP GET variables
        self.form_get = cgi.parse_qs(self.QUERY_STRING, keep_blank_values=1)
        for key in self.form_get.keys():
            if len(self.form_get[key]) == 1:
                self.form_get[key] = self.form_get[key][0]
            else:
                self.form_get[key] = self.form_get[key]

        # Before processing the POST variables, check for "raw" input.
        # We do this by looking at the posted keys (minus the GET
        # keys).  In the case of a raw string post, the key will
        # actually contain the raw string (probably xml or json).  If
        # we do find raw input, we skip form_post processing.
        keys = [k for k in self.form.keys() if not k in self.form_get.keys()]
        if len(keys) == 1 and RE_HTTP_GET_OR_POST_KEY.search(keys.pop()):
            self.form = self.form_get
            self.form_post = {}
            return

        # Create an object to hold only HTTP POST variables
        self.form_post = {}
        for key in self.form:
            if isinstance(self.form[key], list):
                self.form_post[key] = [k.value for k in self.form[key]]
                if key in self.form_get:
                    for v in self.form_get[key]:
                        self.form_post[key].remove(v)

                if isinstance(self.form_post[key], list):
                    if len(self.form_post[key]) == 1:
                        self.form_post[key] = self.form_post[key].pop()

            else:
                self.form_post[key] = self.form[key].value

        # Make sure the form object contains both while taking
        # precedence over POST when overlap exists
        self.form = deepcopy(self.form_get)
        self.form.update(self.form_post)

    def fill(self, env):
        """
        Populate the collection with values.  Some keys contain ``.``
        characters which would break attribute access on this
        collection.  For this reason dots will be replaced with
        underbars.

        :param env: Data to update the env object from
        :type env: :class:`dict`
        """

        for key, value in env.iteritems():
            key = key.replace('.', '_')
            if key in self:
                self[key] = value

    def extras(self):
        """
        Set extra environment variables, all being Chula specific
        """

        self.HTTP_COOKIE = self._cookie()
        self.ajax_uri = self._ajax_uri()

        # Make sure get/post variables are handled correctly
        self._clean_http_vars()
        self._downcast_cgi_vars()
