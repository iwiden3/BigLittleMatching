from try2 import *
import unittest
	#def __init__(self, name, pref, dying_family, twins, has_little):

emily = BigSister('emily', ['rowan', 'marie', 'krista'], 1, 0, 0, 2)
anna = BigSister('anna', ['ella', 'liz', 'sara'], 0, 0, 0, 2)
laura = BigSister('laura', ['sara', 'ella', 'liz'], 0, 0, 0, 2)
bonnie = BigSister('bonnie', ['liz', 'ella', 'sara'], 0, 0, 0, 3)
jess = BigSister('jess', ['rowan', 'krista', 'marie'], 1, 0, 0, 2)
zoey = BigSister('zoey', ['marie', 'rowan', 'krista'], 1, 0, 2, 2)
claire = BigSister('claire', ['marie', 'rowan', 'tina'], 0, 0, 3, 2)

marie = LittleSister('marie', ['emily', 'jess', 'zoey'])
rowan = LittleSister('rowan', ['emily', 'jess', 'zoey'])
ella = LittleSister('ella', ['bonnie', 'laura', 'anna'])
liz = LittleSister('liz', ['anna', 'bonnie', 'laura'])
sara = LittleSister('sara', ['laura', 'anna', 'bonnie'])
krista = LittleSister('krista', ['zoey', 'emily', 'jess'])
tina = LittleSister('tina', ['emily', 'jess', 'zoey'])


big_sisters0 = [anna, laura, bonnie]
big_sisters1 = [emily, jess, zoey]
big_sisters2 = [emily, jess, zoey, claire]

little_sisters0 = [ella, liz, sara]
little_sisters1 = [krista, marie, rowan]
little_sisters2 = [krista, marie, rowan, tina]

result0 = {bonnie : ella, anna : liz, laura : sara}
result1 = {emily : rowan, jess: marie, zoey : krista}

class TestStringMethods(unittest.TestCase):
    
    def test_matches(self):
        self.assertEqual(matches(big_sisters0, little_sisters0), (result0, []))
        self.assertEqual(matches(big_sisters1, little_sisters1), (result1, []))
        self.assertEqual(matches(big_sisters1, little_sisters2), (result1, [tina]))
        self.assertEqual(matches(big_sisters2, little_sisters2), (result1, [tina]))

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