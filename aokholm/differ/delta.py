import copy
import unittest

# remove all of b in a
def removeBinA(a,b, removeOnDiffValues = True):
    for key in b.keys():
        if key in a:
            if type(a[key]) is dict:
                removeBinA(a[key], b[key], removeOnDiffValues)
                if not a[key]: # if the dictionary is empty
                    a.pop(key, None)
            elif a[key] == b[key] or removeOnDiffValues:
                a.pop(key, None)


def setBinA(a,b):
    for key in b.keys():
        if key in a and type(a[key]) is dict:
            setBinA(a[key], b[key])
        else:
            a[key] = b[key]

def merge(a,delta):
    acopy = copy.deepcopy(a)
    setBinA(acopy, delta['set'])
    removeBinA(acopy, delta['delete'])
    return acopy

def delta(a,b):
    delta = {}
    bcopy = copy.deepcopy(b)
    acopy = copy.deepcopy(a)

    removeBinA(bcopy, a, False)
    delta['set'] = bcopy

    removeBinA(acopy,b)
    delta['delete'] = acopy
    return delta

class TestDiffMethods(unittest.TestCase):

    def setUp(self):
        self.dict1 = {
            'a': 'val1a',
            'b': 'val1b',
            'd': {
                'd1': 1,
                'd3': 3
            },
            'e': 10
        }

        self.dict2 = {
            'a': 'Fun',
            'c': 20,
            'd': {
                'd1': 1,
                'd2': [1,2,3,4]
            },
            'e': "mad"
        }

    def test_delta(self):

        result = {
            'set': {'a': {'b': 1}},
            'delete':{}
            }

        self.assertEqual(result, delta({}, {'a': {'b': 1}}))
        self.assertEqual(result, delta({'a': {'b': 2}}, {'a': {'b': 1}}))
        self.assertNotEqual(result, delta({'a': {'b': 1}}, {'a': {'b': 1}}))

        result = {
            'set': {},
            'delete':{'a': {'b': 1}}
            }

        self.assertEqual(result, delta({'a': {'b': 1}}, {}))
        self.assertNotEqual(result, delta({'a': {'b': 1}}, {'a': {'b': 1}}))

        self.assertEqual(self.dict1, delta({}, self.dict1)['set'])
        self.assertEqual(self.dict1, delta(self.dict1, {})['delete'])


    def test_merge(self):
        b1 = {
            'a': {'b': 1},
            'b': {'c': 1, 'd': 2}
        }
        b2 = copy.deepcopy(b1)
        b2['b']['c'] = 2

        self.assertEqual(b1, merge(b2, {
        'set': {'b': {'c': 1}},
        'delete': {}
        }))

        b1 = {
            'a': {'b': 1},
            'b': {'c': 1}
        }
        b2 = copy.deepcopy(b1)
        b2['b']['d'] = 2

        self.assertEqual(b1, merge(b2, {
        'set': {},
        'delete': {'b': {'d': 2}}
        }))

    def test_package(self):
        self.assertEqual(self.dict2, merge(self.dict1, delta(self.dict1, self.dict2)))
        self.assertEqual(self.dict1, merge(self.dict2, delta(self.dict2, self.dict1)))

if __name__ == '__main__':
    unittest.main()
