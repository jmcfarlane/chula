import unittest

from chula import system

class Test_system(unittest.TestCase):
    doctest = system

    def setUp(self):
        self.system = system.System()

    def test_os_type_was_able_to_be_determined(self):
        self.failIf(self.system.type == 'UNKNOWN')

    def test_number_of_processors_able_to_be_determined(self):
        self.failIf(self.system.procs <= 0)
