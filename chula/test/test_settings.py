import unittest
import doctest
from chula import settings
from chula.chulaException import *

class Test_settings(unittest.TestCase):
    def _set(self, key, value):
        self.settings[key] = value 

    def setUp(self):
        self.settings = settings.Settings()

    def test_dict_or_attr_access(self):
        test = 'foo'
        self.settings.session_cache_hosts = test
        self.assertEquals(self.settings['session_cache_hosts'], test)

    def test_valid_key_set(self):
        self.settings.session_cache_hosts = ('')

    def test_invalid_key_set(self):
        self.assertRaises(UnsupportedSettingError, self._set, 'foo', 'bar')

def run_unittest():
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    tests = unittest.makeSuite(Test_settings)
    tests.addTest(doctest.DocTestSuite(settings))
    return tests

if __name__ == '__main__':
    run_unittest()
