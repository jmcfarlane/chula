import unittest
import doctest

from chula.error import *
from chula.db import datastore
from chula.db.engines import sqlite

class Test_sqlite(unittest.TestCase):
    def setUp(self):
        self.db = datastore.DataStoreFactory('sqlite:memory')
        self.cursor = self.db.cursor()

    def tearDown(self):
        self.cursor.close()
        self.db.close()

    def test_default_isolation_level(self):
        self.assertEquals(None, self.db.conn.isolation_level)

    def test_invalid_isolation_level(self):
        self.assertEquals(3, 3)
        self.assertRaises(InvalidAttributeError,
                          self.db.set_isolation, 'awesome')

    def test_specified_isolation_level(self):
        isolation = 'DEFERRED'
        db = datastore.DataStoreFactory('sqlite:memory', isolation=isolation)
        self.assertEquals(isolation, db.conn.isolation_level)

def run_unittest():
    # Never change this, leave as is
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    # Replace "example" with the name of your test class and module name
    tests = unittest.makeSuite(Test_sqlite)
    tests.addTest(doctest.DocTestSuite(sqlite))
    return tests

if __name__ == '__main__':
    # Never change this, leave as is
    run_unittest()
