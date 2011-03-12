"""
Flexible collection that supports both dictionary and attribute style
access.
"""

from copy import deepcopy

from chula import error

class Collection(dict):
    """
    Example usage:

    >>> from chula import collection
    >>> person = collection.Collection()
    >>> person.name = 'Mr. Smith'
    >>> person.age = 20
    >>> person.timezone = 'PST'
    >>>
    >>> print person.age
    20

    >>> print person['timezone']
    PST

    >>> print person
    {'timezone': 'PST', 'age': 20, 'name': 'Mr. Smith'}

    """

    def __delattr__(self, key):
        """
        Allow attribute style deletion

        :param key: Key to be deleted
        :type key: :class:`str`
        """

        self.__delitem__(key)

    def __deepcopy__(self, memo={}):
        """
        Return a fresh copy of a Collection object

        :rtype: :class:`chula.collection.Collection` (filled copy)
        """

        return self.copy_into(self.__class__())

    def copy_into(self, collection):
        """
        Copy the current object into the object passed

        :param collection: Object to be copied into
        :type collection: :class:`chula.collection.Collection`
        :rtype: :class:`chula.collection.Collection` (filled copy)
        """

        for key, value in self.iteritems():
            collection[key] = deepcopy(value)

        return collection

    def __getattr__(self, key):
        """
        Allow attribute style get

        :param key: Key to be accessed
        :type key: :class:`str`
        """

        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError('Attribute not found: %s' % key)

    def __setattr__(self, key, value):
        """
        Allow attribute style set

        :param key: Key to be set
        :type key: :class:`str`
        :param value: Value of key
        :type value: Any
        """

        self.__setitem__(key, value)

    def add(self, key, value):
        """
        Allow set via method

        :param key: Key to be set
        :type key: :class:`str`
        :param value: Value of key
        :type value: Any
        """

        self.__setitem__(key, value)

    def remove(self, key):
        """
        Allow list.remove() style attribute deletion

        :param key: Key/value pair to be removed
        :type key: :class:`str`
        """

        self.__delitem__(key)
