import unittest
import doctest
from chula import collection

class Test_collection(unittest.TestCase):
    def _set(self, key, value):
        self.collection[key] = value 

    def setUp(self):
        self.col = collection.Collection()
        self.col.name = 'foo'
        self.col.location = 'bar'
        self.col.age = 25

    def test_dict_or_attr_access(self):
        test = 'bar'
        self.col.foo = test
        self.assertEquals(self.col['foo'], test)

    def test_valid_key_set(self):
        self.col.foo = ('')

    def test_valid_key_del_by_attr(self):
        self.col.foo = None
        del self.col.foo

    def test_valid_key_del_by_dict(self):
        del self.col['name']
        self.col.remove('age')

    def test_is_iterable_by_iteritems(self):
        data = []
        for key, value in self.col.iteritems():
            data.append(key + ':' + str(value))

        data.sort()
        expected = ['age:25', 'location:bar', 'name:foo']
        self.assertEquals(data, expected)

    def test_is_iterable_by_keys(self):
        i = 0
        keys = list(self.col.keys())
        keys.sort()
        for thing in keys:
            if i == 0:
                self.assertEquals(thing, 'age')
            elif i == 1:
                self.assertEquals(thing, 'location')
            elif i == 2:
                self.assertEquals(thing, 'name')
            i += 1

    def test_is_iterable_by_values(self):
        i = 0
        values = list(self.col.values())
        values.sort()
        for thing in values:
            if i == 0:
                self.assertEquals(thing, 25)
            elif i == 1:
                self.assertEquals(thing, 'bar')
            elif i == 2:
                self.assertEquals(thing, 'foo')
            i += 1

def run_unittest():
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    tests = unittest.makeSuite(Test_collection)
    tests.addTest(doctest.DocTestSuite(collection))
    return tests

if __name__ == '__main__':
    run_unittest()
