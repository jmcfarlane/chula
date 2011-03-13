from random import randrange
import time

# Save cost of the function lookup
_now = time.time

def guid():
    """
    Generate a random guid 64 characters in length.

    :return: :class:`str`

    .. note::

       This module should be removed, and callers updated to use
       :mod:`uuid`.
    """

    def builder():
        now = '%16f-' % _now()
        max = 64 - len(now)
        yield now
        for i in xrange(max):
            # 65=A 91=Z  97=a 122=z
            yield chr(randrange(65, 91))

    return ''.join(builder())
