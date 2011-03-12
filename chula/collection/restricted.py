"""
Collection with a configurable, but enforced number of attributes.
This class is useful for situations where you you need to enforce
every instance of the collection has the exact same structure.
"""

from copy import deepcopy

from chula import error
from chula.collection import base

UNSET = 'THIS ATTRIBUTE NEEDS TO BE SET BY YOU'

class RestrictedCollection(base.Collection):
    """
    Collection class with a pre-determined set of validkeys attributes
    """

    def __init__(self):
        super(RestrictedCollection, self).__init__()
        self.__dict__['privatekeys'] = self.__privatekeys__()
        self.__dict__['validkeys'] = self.__validkeys__()
        self.__defaults__()

        # Ensure defaults have all been set properly
        for key in self.__dict__['validkeys']:
            if not key in self:
                raise error.RestrictecCollectionMissingDefaultAttrError(key)

    def __privatekeys__(self):
        return (())

    def __validkeys__(self):
        return (())

    def __defaults__(self):
        pass

    def __delitem__(self, key):
        """
        Prevent deletion of keys

        :param key: Key to be deleted
        :type key: :class:`str`
        :rtype: :class:`None`
        """

        if key in self.__dict__['validkeys']:
            return super(RestrictedCollection, self).__delitem__(key)
        else:
            raise error.RestrictecCollectionKeyRemovalError(key)

    def __getitem__(self, key):
        """
        Allow restricted attribute access

        :param key: Key to be accessed
        :type key: :class:`str`
        """

        if key in self.__dict__['validkeys']:
            value = super(RestrictedCollection, self).__getitem__(key)
            if value != UNSET:
                return value
            else:
                raise error.RestrictecCollectionMissingDefaultAttrError(key)

        elif key in self.__dict__['privatekeys']:
            return super(RestrictedCollection, self).__getitem__(key)
        else:
            raise error.InvalidCollectionKeyError(key)

    def __setitem__(self, key, value):
        """
        Allow restricted attribute write access

        :param key: Key to be set
        :type key: :class:`str`
        :param value: Value of key
        :type value: Anything
        """

        if key in self.__dict__['validkeys']:
            super(RestrictedCollection, self).__setitem__(key, value)
        elif key in self.__dict__['privatekeys']:
            super(RestrictedCollection, self).__setitem__(key, value)
        else:
            raise error.InvalidCollectionKeyError(key)

    def __delattr__(self, key):
        raise error.RestrictecCollectionKeyRemovalError(key)

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __getstate__(self):
        return self

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setstate__(self, dict_):
        self.__dict__['validkeys'] = dict_.keys()
        self.update(dict_)

    def strip(self):
        """
        Purge *privatekeys* from the collection.  This is useful when
        passing the collection along, without it's private keys.  This
        does actually delete the private keys, and thus acts on
        itself.  If this isn't what you want use :meth:`copy.deepcopy`.
        """

        for key in self.__dict__['privatekeys']:
            super(RestrictedCollection, self).__delitem__(key)

        return self
