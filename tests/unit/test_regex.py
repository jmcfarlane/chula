import unittest
from chula import regex

match = regex.match

class Test_regex(unittest.TestCase):
    doctest = regex

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
