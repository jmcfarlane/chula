"""
Flexible collection that supports both dictionary and attribute style
access.
"""

from chula import error

class Collection(dict):
    def __delattr__(self, key):
        """
        Allow attribute style deletion

        @param key: Key to be deleted
        @type key: String
        """

        self.__delitem__(key)

    def __getattr__(self, key):
        """
        Allow attribute style get
        
        @param key: Key to be accessed
        @type key: String
        @return: Attribute
        """

        return self.__getitem__(key)

    def __setattr__(self, key, value):
        """
        Allow attribute style set
        
        @param key: Key to be set
        @type key: String
        @param value: Value of key
        @type value: Any
        """

        self.__setitem__(key, value)

    def remove(self, key):
        """
        Allow list.remove() style attribute deletion

        @param key: Key/value pair to be removed
        @type key: String
        """

        self.__delitem__(key)


