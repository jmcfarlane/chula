"""
Wrapper class for the Memcache client
"""

from chula import memcache

class Cache(object):
    def __init__(self, servers):
        self.servers = servers
        self.cache = memcache.Client(self.servers, debug=0)

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
        saved = self.cache.set(key, value, minutes * 60)

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
