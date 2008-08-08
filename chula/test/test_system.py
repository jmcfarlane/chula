import unittest
import doctest

from chula import system

class Test_system(unittest.TestCase):
    def setUp(self):
        self.system = system.System()

    def test_os_type_was_able_to_be_determined(self):
        self.failIf(self.system.type == 'UNKNOWN')

    def test_number_of_processors_able_to_be_determined(self):
        self.failIf(self.system.procs <= 0)

def run_unittest():
    # Never change this, leave as is
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    # Replace "example" with the name of your test class and module name
    tests = unittest.makeSuite(Test_system)
    tests.addTest(doctest.DocTestSuite(system))
    return tests

if __name__ == '__main__':
    # Never change this, leave as is
    run_unittest()
