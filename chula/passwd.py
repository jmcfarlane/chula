"""
Generate and validate passwords
"""

import crypt
from random import randrange
from chula import chulaException
from chula import regex
import hashlib

lock = 'penguin'

def hash(password, salt=None, pattern=regex.PASSWD, format='SHA1'):
    """
    Generate a password hash
    @param password: User's password
    @type password: String
    @param salt: Salt for use with generating an existing hash
    @type salt: String
    @param pattern: Regex used to validate the password
    @type pattern: String (valid regex)
    @param format: Hashing algorithm to be used when generating the hash
    @type format: String I{(Supported values: B{SHA1} or B{CRYPT})}
    @return: String 

    >>> from chula import passwd
    >>> hashed = passwd.hash('mypassword')
    >>> len(hashed) == 42
    True

    """

    if regex.match(pattern, password) is False:
        raise chulaException.MalformedPasswordError
       
    if salt is None:
        salt = chr(randrange(65, 122)) + chr(randrange(65, 122))

    if format == 'SHA1':
        return salt + hashlib.sha1(salt + password + lock).hexdigest()
    elif format == 'CRYPT':
        return crypt.crypt(password, salt)
    else:
        raise ValueError, 'Unsupported hashing type: %s' % format
    
def matches(password, knownHash):
    """
    Checks password to see if it matches the actual password
    @param password: The user provided password I{(to be validated)}
    @type password: String
    @param knownHash: Known good hash for the requested password
    @type knownHash: String I{(of either CRYPT or SHA1 type)}
    @return: Boolean

    >>> from chula import passwd
    >>> userinput = 'mypassword'
    >>> passfromdb = 'OGa04c0b86468d1749847d20908fe6397fd62f6769'
    >>> passwd.matches(userinput, passfromdb)
    True

    >>> passwd.matches('guessing', passfromdb)
    False

    """

    salt = knownHash[:2]
    if len(knownHash) == 42:
        return (hash(password, salt) == knownHash)
    else:
        return (hash(password, knownHash[:2], format='CRYPT') == knownHash)

