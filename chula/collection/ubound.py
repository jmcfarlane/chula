"""
Collection that supports a configured maximum size.  The size is
enforced by purging records in a FIFO manner.
"""

from collections import deque

from chula import error
from chula.collection import base

class UboundCollection(base.Collection):
    """
    Collection class with a maximum size
    """

    def __init__(self, max):
        super(UboundCollection, self).__init__()
        self.__dict__['max'] = max
        self.__dict__['fifo'] = deque()

    def __setitem__(self, key, value):
        if len(self.__dict__['fifo']) >= self.__dict__['max']:
            evict = self.__dict__['fifo'].popleft()
            self.remove(evict)

        self.__dict__['fifo'].append(key)
        super(UboundCollection, self).__setitem__(key, value)
