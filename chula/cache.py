"""
Wrapper class for the Memcache client
"""

from chula import error, memcache

class Cache(object):
    def __init__(self, servers):
        self.servers = servers
        self.cache = memcache.Client(self.servers, debug=0)

    @staticmethod
    def clean_key(key):
        if not isinstance(key, basestring):
            msg = 'Cache keys must be of type: str'
            raise error.InvalidCacheKeyError(msg)

        key = list(key)
        for char in key:
            if ord(char) < 33 or ord(char) == 127:
                key.remove(char)

        return ''.join(key)

    def close(self):
        self.cache.disconnect_all()

    def delete(self, key):
        deleted = self.cache.delete(key)

        # Non zero status is success
        if deleted != 0:
            return True
        else:
            return False

    def get(self, key):
        value = self.cache.get(key)
        return value

    def purge(self, key):
        return self.delete(key)

    def set(self, key, value, minutes=1):
        if key != self.clean_key(key):
            msg = "Memcache doesn't support ord < 33 or == 127"
            raise error.InvalidCacheKeyError(msg)

        saved = self.cache.set(key, value, round(minutes * 60))

        # Non zero status is success
        if saved != 0:
            return True
        else:
            return False

    def stats(self):
        servers = []
        stats = self.cache.get_stats()
        for server in stats:
            conn = server[0]
            attrs = server[1]
            attrs['conn'] = conn
            servers.append(attrs)

        return servers
