import unittest
import doctest
from chula import regex

match = regex.match

class Test_regex(unittest.TestCase):
    def test_ipv4(self):
        self.assertEqual(match(regex.IPV4, '127.0.0.1'), True)
        self.assertEqual(match(regex.IPV4, '12x.0.0.1'), False)

    def test_passwd_special_chars(self):
        self.assertEqual(match(regex.PASSWD, 'abcdefg'), True)
        self.assertEqual(match(regex.PASSWD, '123456'), True)
        self.assertEqual(match(regex.PASSWD, '!@#$%^&*?.'), True)

    def test_passwd_illegal_chars(self):
        self.assertEqual(match(regex.PASSWD, r'~`()[]{}\/<>,|'), False)

    def test_passwd_at_least_six_chars(self):
        self.assertEqual(match(regex.PASSWD, '12345'), False)
        self.assertEqual(match(regex.PASSWD, '123456'), True)

def run_unittest():
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    tests = unittest.makeSuite(Test_regex)
    tests.addTest(doctest.DocTestSuite(regex))
    return tests

if __name__ == '__main__':
    run_unittest()
