import copy
import cPickle
import unittest

from chula import collection, json
from chula.collection import base

class Test_base_collection(unittest.TestCase):
    doctest = base

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

    def test_encode_by_cpickle(self):
        encoded = cPickle.dumps(self.col)
        self.assertEquals(type(encoded), type('string'))

    def test_decode_by_cpickle(self):
        encoded = cPickle.dumps(self.col)
        decoded = cPickle.loads(encoded)
        self.assertEquals(decoded.age, self.col.age)
        self.assertEquals(decoded.location, self.col.location)
        self.assertEquals(decoded.name, self.col.name)
        self.assertEquals(type(decoded), type(collection.Collection()))
        
    def test_encode_by_json(self):
        encoded = json.encode(self.col)
        self.assertEquals(type(encoded), type('string'))

    def test_decode_by_json(self):
        encoded = json.encode(self.col)
        decoded = json.decode(encoded)
        self.assertEquals(decoded['age'], self.col.age)
        self.assertEquals(decoded['location'], self.col.location)
        self.assertEquals(decoded['name'], self.col.name)
        self.assertEquals(type(decoded), type({}))

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

    def test_deepcopy(self):
        freshcopy = copy.deepcopy(self.col)
        self.assertEquals(freshcopy.name, 'foo')
        self.assertEquals(freshcopy.location, 'bar')
        self.assertEquals(freshcopy.age, 25)
        self.assertEquals(True, isinstance(freshcopy, collection.Collection))
