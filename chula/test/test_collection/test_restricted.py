import unittest
import doctest
import copy

from chula import collection
from chula.collection import restricted
from chula.error import *

# Example usage of RestrictedCollection class to test it
class Human(collection.RestrictedCollection):
    def __validkeys__(self):
        return ('head', 'leg', 'arm', 'foot')

    # TODO: Fix this huge mess, why can't the base class do it!!
    def __deepcopy__(self, memo={}):
        """
        Return a fresh copy of a Collection object or subclass object
        """
        
        fresh = Human()
        for key, value in self.iteritems():
            fresh[key] = copy.deepcopy(value, memo)

        return fresh

    def __defaults__(self):
        self.head = 'wears hat'
        self.leg = 'two to walk with'
        self.arm = 'hold coffee with'
        self.foot = 'smell'

class Test_restricted_collection(unittest.TestCase):
    def setUp(self):
        self.human = Human()

    def test_key_with_defalt(self):
        self.assertEquals(self.human.head, 'wears hat')
        self.assertEquals(self.human.foot, 'smell')

    def test_key_no_default(self):
        def simulate():
            class Human(collection.RestrictedCollection):
                def __validkeys__(self):
                    return ('head', 'stomach')

                def __defaults__(self):
                    self.head = 'wears hat'

            person = Human()

        self.assertRaises(RestrictecCollectionMissingDefaultAttrError,
                          simulate)

    def test_get_invalid_attr(self):
        def simulate():
            return self.human.missing

        self.assertRaises(InvalidCollectionKeyError, simulate)
        
    def test_get_invalid_dict(self):
        def simulate():
            return self.human['missing']

        self.assertRaises(InvalidCollectionKeyError, simulate)

    def test_set_invalid_attr(self):
        def simulate():
            self.human.back = 'important'

        self.assertRaises(InvalidCollectionKeyError, simulate)
        
    def test_set_invalid_dict(self):
        def simulate():
            self.human['back'] = 'important'

        self.assertRaises(InvalidCollectionKeyError, simulate)
        
    def test_deepcopy(self):
        person = copy.deepcopy(self.human)
        self.assertEquals(person.head, 'wears hat')
        self.assertEquals(person.foot, 'smell')
        self.assertEquals(True, isinstance(person, collection.Collection))

        # TODO: This needs to pass
        self.assertEquals(True, isinstance(person,
                                           collection.RestrictedCollection))
        
def run_unittest():
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    tests = unittest.makeSuite(Test_restricted_collection)
    tests.addTest(doctest.DocTestSuite(restricted))
    return tests

if __name__ == '__main__':
    run_unittest()
