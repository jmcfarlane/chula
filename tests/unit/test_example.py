import unittest

from chula import example

class Test_example(unittest.TestCase):
    doctest = example

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
