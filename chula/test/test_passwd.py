import unittest
import doctest
from chula import passwd
from chula.chulaException import *

password = 'cookiemonster'
salt = 'ai'
sha1 = 'ai0ea9191b374fad28b17c18e1f45a3140868ba402'
crypted = 'aiLgRTdyZEqEw'

class Test_passwd(unittest.TestCase):
    def test_new_password_with_known_hash(self):
        self.assertEquals(sha1, passwd.hash(password, salt=salt))

    def test_old_password_with_known_hash(self):
        hash = passwd.hash(password, salt='ai', format='CRYPT')
        self.assertEquals(crypted, hash)

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

    def test_old_matches_with_positive_match(self):
        self.assertTrue(passwd.matches(password, crypted))
    
    def test_old_matches_without_positive_match(self):
        self.assertFalse(passwd.matches('badpasswd', crypted))

def run_unittest():
    # Never change this, leave as is
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    tests = unittest.makeSuite(Test_passwd)
    tests.addTest(doctest.DocTestSuite(passwd))
    return tests

if __name__ == '__main__':
    # Never change this, leave as is
    run_unittest()
