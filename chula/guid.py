import time
from random import randrange

# Save cost of the function lookup
_now = time.time

def guid():
    """
    Generate a random guid 64 characters in length.
    @return: String
    """
    
    parts = []
    now = _now()
    # Save cost of function lookup
    append = parts.append

    parts.append('%016x' % now)
    for i in xrange(64 - len(parts[0])):
        # 65=A 91=Z  97=a 122=z
        append(chr(randrange(65, 91)))

    return ''.join(parts)
