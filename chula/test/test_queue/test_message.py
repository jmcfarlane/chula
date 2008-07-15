import unittest
import doctest

from chula import collection
from chula.queue import message

config = collection.Collection()
config.mqueue_db = 'sqlite:memory'

class Test_mqueue(unittest.TestCase):
    def setUp(self):
        self.mqueue = message.MessageQueue(config)

    def tearDown(self):
        self.mqueue.close()

    def test_schema(self):
        self.assertEquals(True, self.mqueue.schema_exists())

    def test_add(self):
        self.mqueue.add('testing')

    def test_pop_return_value(self):
        keys_expected = ['id', 'name', 'processed', 'timestamp']
        keys_expected.sort()

        self.mqueue.add('testing')
        msg = self.mqueue.pop()
        keys_found = msg.keys()
        keys_found.sort()
        self.assertEquals(keys_expected, keys_found)
        self.assertEquals(True, isinstance(msg, message.Message))

    def test_pop_delete(self):
        self.mqueue.add('testing')
        msg = self.mqueue.pop()
        msg = self.mqueue.pop()
        self.assertEquals(None, msg)

def run_unittest():
    # Never change this, leave as is
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    # Replace "example" with the name of your test class and module name
    tests = unittest.makeSuite(Test_mqueue)
    tests.addTest(doctest.DocTestSuite(message))
    return tests

if __name__ == '__main__':
    # Never change this, leave as is
    run_unittest()
