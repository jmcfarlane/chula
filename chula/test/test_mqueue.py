import unittest
import doctest

from chula import collection, mqueue

class Test_mqueue(unittest.TestCase):
    def setUp(self):
        config = collection.Collection()
        config.mqueue_db = 'sqlite:memory'
        self.mqueue = mqueue.MessageQueue(config)
        self.mqueue.connect()

    def tearDown(self):
        pass
        self.mqueue.close()

    def test_00_connect(self):
        pass

    def test_schema_created(self):
        pass

def run_unittest():
    # Never change this, leave as is
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    # Replace "example" with the name of your test class and module name
    tests = unittest.makeSuite(Test_mqueue)
    tests.addTest(doctest.DocTestSuite(mqueue))
    return tests

if __name__ == '__main__':
    # Never change this, leave as is
    run_unittest()
