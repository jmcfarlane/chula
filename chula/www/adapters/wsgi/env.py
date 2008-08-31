"""
Manage the environment when python is using wsgi
"""

import cgi
import re

from chula.www.adapters import env

class Environment(env.BaseEnv):
    def __init__(self, environ):
        super(Environment, self).__init__()

        # Update the environment with wsgi properties
        for key, value in environ.iteritems():
            key = key.replace('.', '_')
            if key in self:
                self[key] = value

        # Make sure HTTP_COOKIE exists even if empty
        self.HTTP_COOKIE = environ.get('HTTP_COOKIE', {})

        # Set ajax_uri
        # TODO: (move to the baseclass if possible)
        protocol_type = re.match(r'(HTTPS?)', self.SERVER_PROTOCOL)
        if not protocol_type is None:
            protocol_type = protocol_type.group()
        else:
            msg = 'Unsupported protocol: %s' % self.SERVER_PROTOCOL
            raise ValueError(msg)

        self.ajax_uri = protocol_type.lower() + '://' + self.HTTP_HOST

        # HTTP variables
        #foo = self.wsgi_input.readlines()
        #if len(foo) > 0:
        #    raise Exception(str(foo))

        form = cgi.FieldStorage(fp=self.wsgi_input,
                                environ=environ,
                                keep_blank_values=1)
        for key in form.keys():
            self.form[key] = form[key].value
