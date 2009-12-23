"""Chula memcached based session store"""

import hashlib

from chula import logger, memcache
from chula.session.backends import base

LOG = logger.Logger().logger('chula.session.backends.memcached')

class Backend(base.Backend):
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

    def destroy(self, guid):
        self.connect()

        if not self.conn is None:
            return self.conn.delete(self.mkey(guid))

        return False

    def fetch_session(self, guid):
        self.connect()

        values = self.conn.get(self.mkey(guid))
        if values is None:
            LOG.debug('Did not find session, guid: %s' % guid)
            return None
        else:
            LOG.debug('length of string in cache: %s' % len(values))
            return values
   
    def mkey(self, guid):
        """
        Hash the key to avoid character escaping and the >255 character
        limitation of cache keys.

        @return: SHA1 hash
        """
        
        return hashlib.sha1('session:%s' % guid).hexdigest()
    
    def persist(self, guid, encoded):
        self.connect()
        key = self.mkey(guid)

        if isinstance(self.conn, memcache.Client):
            # Non zero status is success
            if self.conn.set(key, encoded, self.config.session_timeout * 60) != 0:
                return True

        return False
