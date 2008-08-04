import unittest
import doctest

from chula import collection
from chula.collection import ubound
from chula.error import *

class Test_ubound_collection(unittest.TestCase):
    def _fetch_by_key(self, key):
        return self.collection[key]

    def setUp(self):
        self.collection = collection.UboundCollection(5)
        self.collection.a = 1
        self.collection.b = 2
        self.collection.c = 3
        self.collection.d = 4
        self.collection.e = 5

    def tearDown(self):
        pass

    def test_initial_length(self):
        self.collection = collection.UboundCollection(5)
        self.assertEquals(0, len(self.collection))

    def test_allows_specified_max_records(self):
        self.assertEquals(5, len(self.collection))
        self.assertEquals(1, self.collection.a)

    def test_purging_does_purge_FIFO_by_attr(self):
        self.collection.f = 6
        
        self.assertEquals(5, len(self.collection))
        self.assertRaises(KeyError, self._fetch_by_key, 'a')

    def test_purging_does_purge_FIFO_by_key(self):
        self.collection['f'] = 6
        
        self.assertEquals(5, len(self.collection))
        self.assertRaises(KeyError, self._fetch_by_key, 'a')

def run_unittest():
    # Never change this, leave as is
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    # Replace "example" with the name of your test class and module name
    tests = unittest.makeSuite(Test_ubound_collection)
    tests.addTest(doctest.DocTestSuite(ubound))
    return tests

if __name__ == '__main__':
    # Never change this, leave as is
    run_unittest()
