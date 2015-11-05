from try2 import *
import unittest
	#def __init__(self, name, pref, dying_family, twins, has_little):

emily = BigSister('emily', ['rowan', 'marie', 'krista'], 1, 0, 0)
marie = LittleSister('marie', ['emily', 'jess', 'zoey'])
rowan = LittleSister('rowan', ['emily', 'jess', 'zoey'])

class TestStringMethods(unittest.TestCase):
    def test_match(self):
        result = {}
        self.assertEqual(match(emily, marie, result), (True, None))
        self.assertEqual(result[emily], marie)
        self.assertEqual(match(emily, rowan, result), (True, marie))
        self.assertEqual(result[emily], rowan)
        self.assertEqual(match(emily, marie, result), (False, None))
        self.assertEqual(result[emily], rowan)


if __name__ == '__main__':
    unittest.main()