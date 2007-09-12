"""
Flexible collection that supports both dictionary and attribute style
access.
"""

class Collection(object):
    def __init__(self):
        self.__dict__['_keys'] = set()

    def iteritems(self):
        for key in self._keys:
            yield (key, self.__dict__[key])

    def keys(self):
        return tuple(self._keys)

    def remove(self, key):
        self.__delattr__(key)

    def values(self):
        for key in self.__dict__.keys():
            if key in self._keys:
                yield self.__dict__[key]

    def __contains__(self, key):
        if key in self.__dict__['_keys']:
            return True
        else:
            return False

    def __delattr__(self, key):
        del self.__dict__[key]
        self._keys.remove(key)

    def __getattr__(self, key):
        return self.__dict__[key]

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        self._keys.add(key)

    # Also allow dictionary style access
    def __delitem__(self, key):
        self.__delattr__(key)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

