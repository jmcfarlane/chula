"""
Manage the environment when python is using mod_python
"""

import re

from mod_python import util

from chula.www.adapters import env

class Environment(env.BaseEnv):
    def __init__(self, req):
        super(Environment, self).__init__()

        # Set the required variables from mod_python's req object(s)
        self.DOCUMENT_ROOT = req.document_root()
        self.HTTP_HOST = req.hostname
        self.HTTP_USER_AGENT = req.headers_in.get('User-Agent')
        self.REQUEST_URI = req.unparsed_uri
        self.SERVER_PROTOCOL = req.protocol
        self.HTTP_COOKIE = req.headers_in.get('Cookie')

        # TODO: Implement these
        self.GATEWAY_INTERFACE = 'MOD_PYTHON'
        self.HTTP_ACCEPT = 'NA'
        self.HTTP_ACCEPT_CHARSET = 'NA'
        self.HTTP_ACCEPT_ENCODING = 'NA'
        self.HTTP_ACCEPT_LANGUAGE = 'NA'
        self.HTTP_CONNECTION = 'NA'
        self.HTTP_KEEP_ALIVE = 'NA'
        self.PATH = 'NA'
        self.PATH_INFO = 'NA'
        self.QUERY_STRING = 'NA'
        self.REMOTE_ADDR = 'NA'
        self.REMOTE_HOST = 'NA'
        self.REMOTE_PORT = 'NA'
        self.REQUEST_METHOD = 'NA'
        self.SCRIPT_FILENAME = 'NA'
        self.SCRIPT_NAME = 'NA'
        self.SERVER_ADDR = 'NA'
        self.SERVER_ADMIN = 'NA'
        self.SERVER_NAME = 'NA'
        self.SERVER_PORT = 'NA'
        self.SERVER_SIGNATURE = 'NA'
        self.SERVER_SOFTWARE = 'NA'

        # If self.req.form exists and is of type util.FieldStorage
        # trust it's contents and move on, else set it (currently to
        # the same value that mod_python publisher would set it).
        try:
            if isinstance(self.req.form, util.FieldStorage):
                return
        except:
            self.form = util.FieldStorage(req, keep_blank_values=1)

        self.form = dict(self.form)

        # Set ajax_uri
        # TODO: (move to the baseclass if possible)
        protocol_type = re.match(r'(HTTPS?)', self.SERVER_PROTOCOL)
        if not protocol_type is None:
            protocol_type = protocol_type.group()
        else:
            msg = 'Unsupported protocol: %s' % self.SERVER_PROTOCOL
            raise ValueError(msg)

        self.ajax_uri = protocol_type.lower() + '://' + self.HTTP_HOST
