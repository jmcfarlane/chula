"""Chula memcached based session store"""

import hashlib

from chula import logger
from chula.session.backends import base
from chula.vendor import memcache

class Backend(base.Backend):
    def __init__(self, config, guid):
        super(Backend, self).__init__(config, guid)
        self.connect()
        self.calculate_key()
        self.log = logger.Logger(config).logger('chula.session.memcached')


    def gc(self):
        try:
            self.conn.disconnect_all()
        except:
            pass
        finally:
            self.conn = None

    def connect(self):
        if not isinstance(self.conn, memcache.Client):
            self.conn = memcache.Client(self.config.session_memcache, debug=0)

    def destroy(self):
        self.connect()

        if not self.conn is None:
            return self.conn.delete(self.key)

        return False

    def fetch_session(self):
        self.connect()

        values = self.conn.get(self.key)
        if values is None:
            self.log.debug('Did not find session, guid: %s' % self.guid)
            return None
        else:
            self.log.debug('Session found: OK')
            return values
   
    def calculate_key(self):
        """
        Hash the key to avoid character escaping and the >255 character
        limitation of cache keys.

        @return: SHA1 hash
        """
        
        self.key = hashlib.sha1('session:%s' % self.guid).hexdigest()
        return self.key
    
    def persist(self, encoded):
        self.connect()
        timeout = self.config.session_timeout * 60

        if isinstance(self.conn, memcache.Client):
            # Non zero status is success
            if self.conn.set(self.key, encoded, timeout) != 0:
                return True

        return False
