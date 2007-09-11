import unittest
import doctest
from chula import config
from chula.chulaException import *

class Test_config(unittest.TestCase):
    def _set(self, key, value):
        self.config[key] = value 

    def setUp(self):
        self.config = config.Config()

    def test_dict_or_attr_access(self):
        test = 'foo'
        self.config.session_cache_hosts = test
        self.assertEquals(self.config['session_cache_hosts'], test)

    def test_valid_key_set(self):
        self.config.session_cache_hosts = ('')

    def test_invalid_key_set(self):
        self.assertRaises(UnsupportedConfigError, self._set, 'foo', 'bar')

def run_unittest():
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    tests = unittest.makeSuite(Test_config)
    tests.addTest(doctest.DocTestSuite(config))
    return tests

if __name__ == '__main__':
    run_unittest()
