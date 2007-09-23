import unittest
import doctest
from chula import example

class Test_example(unittest.TestCase):
    def setUp(self):
        self.something = 'This gets reset at the start of every test'
        self.db = 'Sometimes you will set a db and cursor here'
        self.example = example.Example()

    def tearDown(self):
        self.something = 'This resets it after each test'

    def test_something(self):
        self.assertEquals([], example.something())

    def test_sum(self):
        self.assertEquals(3, self.example.sum(1, 2))
        self.assertRaises(TypeError, self.example.sum, (1, '2'))

    def test_awesome(self):
        self.failIf(not self.example.awesome())

def run_unittest():
    # Never change this, leave as is
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    # Replace "example" with the name of your test class and module name
    tests = unittest.makeSuite(Test_example)
    tests.addTest(doctest.DocTestSuite(example))
    return tests

if __name__ == '__main__':
    # Never change this, leave as is
    run_unittest()
