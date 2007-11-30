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


UNSET = 'THIS ATTRIBUTE NEEDS TO BE SET BY YOU'
class RestrictedCollection(Collection):
    """
    Collection class with a pre-determined set of validkeys attributes
    """

    def __init__(self):
        super(RestrictedCollection, self).__init__()
        self.__dict__['validkeys'] = self.__validkeys__()
        self.__defaults__()

        # Ensure defaults have all been set properly
        for key in self.__dict__['validkeys']:
            if not key in self:
                raise error.RestrictecCollectionMissingDefaultAttrError(key)

    def __validkeys__(self):
        return (())

    def __defaults__(self):
        pass

    def __delitem__(self, key):
        """
        Prevent deletion of keys

        @param key: Key to be deleted
        @type key: String
        @return: None
        """

        if key in self.__dict__['validkeys']:
            return super(RestrictedCollection, self).__delitem__(key)
        else:
            raise error.RestrictecCollectionKeyRemovalError(key)

    def __getitem__(self, key):
        """
        Allow restricted attribute access

        @param key: Key to be accessed
        @type key: String
        @return: Attribute
        """

        if key in self.__dict__['validkeys']:
            value = super(RestrictedCollection, self).__getitem__(key)
            if value != UNSET:
                return value
            else:
                raise error.RestrictecCollectionMissingDefaultAttrError(key)
        else:
            raise error.InvalidCollectionKeyError(key)

    def __setitem__(self, key, value):
        """
        Allow restricted attribute write access

        @param key: Key to be set
        @type key: String
        @param value: Value of key
        @type value: Anything
        """

        if key in self.__dict__['validkeys']:
            super(RestrictedCollection, self).__setitem__(key, value)
        else:
            raise error.InvalidCollectionKeyError(key)

    def __delattr__(self, key):
        raise error.RestrictecCollectionKeyRemovalError(key)
        
    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
