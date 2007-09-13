"""
Flexible collection that supports both dictionary and attribute style
access.
"""

class Collection(dict):
    def __delattr__(self, key):
        self.__delitem__(key)

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def remove(self, key):
        self.__delitem__(key)
