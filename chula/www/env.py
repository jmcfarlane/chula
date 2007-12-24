"""
Environment variables
"""

import re

from chula import collection

class Env(collection.Collection):
    def __init__(self, req):
        super(Env, self).__init__()
        
        # mod_python req variables
        self.args = req.args
        self.content_type = req.content_type
        self.document_root = req.document_root()
        self.filename = req.filename
        self.hostname = req.hostname
        self.method = req.method
        self.path_info = req.path_info
        self.proto_num = req.proto_num
        self.protocol = req.protocol
        self.status = req.status
        self.the_request = req.the_request
        self.unparsed_uri = req.unparsed_uri
        self.uri = req.uri

        # mod_python req.connection variables
        conn = req.connection
        self.local_addr = conn.local_addr
        self.local_host = conn.local_host
        self.remote_addr = conn.remote_addr
        self.remote_host = conn.remote_host
        self.remote_ip = conn.remote_ip

        # mod_python req.headers_in variables
        headers = req.headers_in.get
        self.host = headers('host')
        self.referer = headers('Referer')
        self.user_agent = headers('User-Agent')

        # Check for broken variables
        if self.host is None:
            self.host = '%s:%s' % (self.hostname, self.local_addr[1])

        # Computed variables
        self.protocol_type = re.match(r'(HTTPS?)', self.protocol).group()
        self.ajax_uri = self.protocol_type.lower() + '://' + self.host

        # Misc variables
        self.debug = False
