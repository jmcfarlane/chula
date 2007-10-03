"""
Generate and validate passwords
"""

import hashlib
from random import randrange

from chula import error, regex

lock = 'chula-salt'
SALT_LENGTH = 6

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
    >>> len(hashed) == 46
    True
    """

    if not regex.match(pattern, password):
        raise error.MalformedPasswordError
       
    if salt is None:
        def generate_salt():
            for i in xrange(SALT_LENGTH):
                yield chr(randrange(65, 122))

        salt = ''.join(generate_salt())

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
    >>> pass_from_db = '^Bo\\Jcc16b5dae81478c1ab4655dd69df121e87ea43a2f'
    >>> passwd.matches(user_input, pass_from_db)
    True

    >>> passwd.matches('guessing', pass_from_db)
    False
    """

    salt = known_hash[:SALT_LENGTH]

    return hash(password, salt) == known_hash
