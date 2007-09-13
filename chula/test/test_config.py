import unittest
import doctest
from chula import config
from chula.chulaException import *

class Test_config(unittest.TestCase):
    def d_set(self, key, value):
        self.config[key] = value 

    def a_set(self, key, value):
        setattr(self.config, key, value)

    def setUp(self):
        self.config = config.Config()

    def test_valid_key_set(self):
        self.config.session_memcache = ('')
        self.config['classpath'] = 'foo'

    def test_invalid_key_set_by_dict(self):
        self.assertRaises(UnsupportedConfigError, self.d_set, 'foo', 'bar')

    def test_invalid_key_set_by_attr(self):
        self.assertRaises(UnsupportedConfigError, self.a_set, 'foo', 'bar')

def run_unittest():
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    tests = unittest.makeSuite(Test_config)
    tests.addTest(doctest.DocTestSuite(config))
    return tests

if __name__ == '__main__':
    run_unittest()
