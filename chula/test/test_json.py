import unittest
import doctest
from chula import json

class Test_json(unittest.TestCase):
    def test_encode_dict(self):
        """
        Tests encoding of a dictionary to JSON
        """
        myDict = {"apple":1, "bear":2, "lion":3}
        myJSON = json.encode(myDict)
        self.assertEqual(myJSON, '{"lion": 3, "apple": 1, "bear": 2}')
    def test_decode_dict(self):
        """
        Tests decoding of JSON to dictionary
        """
        myJSON = '{"lion": 3, "apple": 1, "bear": 2}'
        myDict = json.decode(myJSON)
        self.assertEqual(myDict, {"lion": 3, "apple": 1, "bear": 2})
    def test_encode_list(self):
        """
        Tests encoding of a list to JSON
        """
        myList = ["apple", "orange", "plum", "pear"]
        myJSON = json.encode(myList)
        self.assertEqual(myJSON, '["apple", "orange", "plum", "pear"]')
    def test_decode_list(self):
        """
        Tests decoding of JSON to a list
        """
        myJSON = '["apple", "orange", "plum", "pear"]'
        myList = json.decode(myJSON)
        self.assertEqual(myList, ["apple", "orange", "plum", "pear"])
    def test_invalid_json(self):
        """
        Tests json for issues that should cause exceptions but might fail
        to
        """
        try:
            myJSON = '{1"lion": 3, "apple": 1, "bear": 2}'
            myDict = json.decode(myJSON)
        except ValueError, ex:
            pass
        else:
            raise Exception, \
                "chula.json decoded invalid JSON: %s" % myJSON
        try:
            myJSON = {"lion": 3, "apple": 1, "bear": 2}
            myDict = json.decode(myJSON)
        except TypeError, ex:
            pass
        else:
            raise Exception, \
                "chula.json decoded invalid JSON: %s" % myJSON


def run_unittest():
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    tests = unittest.makeSuite(Test_json)
    tests.addTest(doctest.DocTestSuite(json))
    return tests

if __name__ == '__main__':
    run_unittest()
