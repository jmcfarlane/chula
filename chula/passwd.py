"""
Generate and validate passwords
"""

import hashlib
from random import randrange

from chula import chulaException, regex

lock = 'penguin'

def hash(password, salt=None, pattern=regex.PASSWD):
    """
    Generate a password hash
    @param password: User's password
    @type password: String
    @param salt: Salt for use with generating an existing hash
    @type salt: String
    @param pattern: Regex used to validate the password
    @type pattern: String (valid regex)
    @return: String 

    >>> from chula import passwd
    >>> hashed = passwd.hash('mypassword')
    >>> len(hashed) == 42
    True
    """

    if not regex.match(pattern, password):
        raise chulaException.MalformedPasswordError
       
    if salt is None:
        salt = chr(randrange(65, 122)) + chr(randrange(65, 122))

    return salt + hashlib.sha1(salt + password + lock).hexdigest()
    
def matches(password, knownHash):
    """
    Checks password to see if it matches the actual password
    @param password: The user provided password I{(to be validated)}
    @type password: String
    @param knownHash: Known good hash for the requested password
    @type knownHash: String
    @return: Boolean

    >>> from chula import passwd
    >>> userinput = 'mypassword'
    >>> passfromdb = 'abc09b160099a8cde4e422015f195d1b0b5655dabf2'
    >>> passwd.matches(userinput, passfromdb)
    True

    >>> passwd.matches('guessing', passfromdb)
    False
    """

    salt = knownHash[:3]
    return (hash(password, salt) == knownHash)
