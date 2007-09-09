import unittest
import doctest
from chula import guid
import time

class Test_guid(unittest.TestCase):
    def msg(self):
        msg = 'Guid generation was too slow: %s ms > %s ms'
        return msg % (round(self.speed / self.tests, 5),
                      self.max)

    def fastEnough(self):
        return self.speed / self.tests < self.max

    def unique(self, max=50):
        unique = set()
        for x in xrange(max):
            unique.add(guid.guid())
        return len(unique)

    def setUp(self):
        self.start = time.time()
        self.max = 0.0005 # Unit of measure is second per guid generation
        self.uv = 'Unique violation: guid() generated a non unique guid!'

    def test_500(self):
        self.tests = 500
        self.assertEqual(self.tests, self.unique(self.tests), self.uv)
        self.speed = time.time() - self.start
        self.assertTrue(self.fastEnough(), self.msg())

    def test_5000(self):
        self.tests = 5000
        self.assertEqual(self.tests, self.unique(self.tests), self.uv)        
        self.speed = time.time() - self.start
        self.assertTrue(self.fastEnough(), self.msg())

def run_unittest():
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    tests = unittest.makeSuite(Test_guid)
    tests.addTest(doctest.DocTestSuite(guid))
    return tests

if __name__ == '__main__':
    run_unittest()
