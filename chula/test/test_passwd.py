import unittest
from chula import passwd
from chula.error import *

password = 'gitisbetterthancvs'
sha1 = 'NcA_puae9ca8739ddfd7db27c153015d39bc5d8c47b345'
salt = sha1[:passwd.SALT_LENGTH]

class Test_passwd(unittest.TestCase):
    doctest = passwd

    def test_new_password_with_known_hash(self):
        self.assertEquals(sha1, passwd.hash(password, salt=salt))

    def test_similar_passwords_are_unique_with_salt(self):
        self.assertNotEqual(passwd.hash(password, salt=salt),
                            passwd.hash('cookiemonseterMM', salt=salt))

    def test_similar_passwords_are_unique_without_salt(self):
        self.assertNotEqual(passwd.hash(password),
                            passwd.hash('cookiemonseterMM'))

    def test_malformed_password(self):
        self.assertRaises(MalformedPasswordError, passwd.hash, 'a')

    def test_new_matches_with_positive_match(self):
        self.assertTrue(passwd.matches(password, sha1))

    def test_new_matches_without_positive_match(self):
        self.assertFalse(passwd.matches('badpasswd', sha1))
