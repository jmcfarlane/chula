import unittest
import doctest
from chula import config
from chula.error import *

class Test_config(unittest.TestCase):
    def d_set(self, key, value):
        self.config[key] = value 

    def a_set(self, key, value):
        setattr(self.config, key, value)

    def d_get(self, key):
        foo = self.config[key]

    def a_get(self, key):
        foo = self.config.key

    def setUp(self):
        self.config = config.Config()

    def test_valid_key_set(self):
        self.config.session_memcache = ('')
        self.config['classpath'] = 'foo'

    def test_keys_method_not_destroyed(self):
        self.assertEquals(len(self.config.keys()), 15)

    def test_printing_not_result_in_empty_dict(self):
        self.assertTrue(isinstance(self.config, dict))
        self.assertNotEquals(str(self.config), '{}')

    def test_invalid_key_set_by_dict(self):
        self.assertRaises(InvalidCollectionKeyError, self.d_set, 'foo', 'bar')

    def test_invalid_key_set_by_attr(self):
        self.assertRaises(InvalidCollectionKeyError, self.a_set, 'foo', 'bar')

    def test_invalid_key_get_by_dict(self):
        self.assertRaises(InvalidCollectionKeyError, self.d_get, 'foo')

    def test_invalid_key_get_by_attr(self):
        self.assertRaises(InvalidCollectionKeyError, self.a_get, 'foo')

    def test_default_value_inforced_when_UNSET(self):
        error = RestrictecCollectionMissingDefaultAttrError
        self.assertRaises(error, self.d_get, 'classpath')

def run_unittest():
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    tests = unittest.makeSuite(Test_config)
    tests.addTest(doctest.DocTestSuite(config))
    return tests

if __name__ == '__main__':
    run_unittest()
