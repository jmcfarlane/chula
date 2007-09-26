"""
Generate and validate passwords
"""

import hashlib
from random import randrange

from chula import error, regex

lock = 'chula-salt'

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
        raise error.MalformedPasswordError
       
    if salt is None:
        salt = chr(randrange(65, 122)) + chr(randrange(65, 122))

    return salt + hashlib.sha1(salt + password + lock).hexdigest()
    
def matches(password, known_hash):
    """
    Checks password to see if it matches the actual password
    @param password: The user provided password I{(to be validated)}
    @type password: String
    @param known_hash: Known good hash for the requested password
    @type known_hash: String
    @return: bool

    >>> from chula import passwd
    >>> user_input = 'mypassword'
    >>> pass_from_db = 'abcb1b32c7848bac608f33c4464aab928a0bc1c2e57'
    >>> passwd.matches(user_input, pass_from_db)
    True

    >>> passwd.matches('guessing', pass_from_db)
    False
    """

    salt = known_hash[:3]

    return hash(password, salt) == known_hash
