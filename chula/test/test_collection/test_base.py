import unittest
import doctest

from chula import collection
from chula.collection import base

class Test_base_collection(unittest.TestCase):
    def _get(self, key):
        return self.col[key]

    def setUp(self):
        self.col = collection.Collection()
        self.col.name = 'foo'
        self.col.location = 'bar'
        self.col.age = 25

    def test_access_by_get(self):
        self.assertEquals(self.col.get('name'), 'foo')

    def test_access_by_attribute(self):
        self.assertEquals(self.col.name, 'foo')

    def test_access_by_dict(self):
        self.assertEquals(self.col['name'], 'foo')

    def test_access_by_iteritems(self):
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

    def test_set_by_add(self):
        self.col.add('foo', 'bar')
        self.assertEquals(self.col.foo, 'bar')

    def test_set_by_attr(self):
        self.col.foo = None
        self.assertEquals(self.col.foo, None)

    def test_set_by_dict(self):
        self.col['foo'] = None
        self.assertEquals(self.col.foo, None)

    def test_missing_key_raises_key_error(self):
        self.assertRaises(KeyError, self._get, 'missing')

    def test_can_delete_by_attr(self):
        self.col.foo = None
        del self.col.foo

    def test_can_delete_by_dict(self):
        del self.col['name']
        self.assertRaises(KeyError, self._get, 'name')

    def test_can_delete_by_remove_method(self):
        self.col.remove('name')
        self.assertRaises(KeyError, self._get, 'name')

def run_unittest():
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    tests = unittest.makeSuite(Test_base_collection)
    tests.addTest(doctest.DocTestSuite(base))
    return tests

if __name__ == '__main__':
    run_unittest()
