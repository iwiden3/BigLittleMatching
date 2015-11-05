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
rhianna = BigSister('rhianna', ['a', 'b', 'c'], 1, 0, 0, 2)
molly = BigSister('molly', ['tara', 'hara', 'jana'], 1, 0, 0, 2)
ariel = BigSister('ariel', ['lane', 'mara', 'zenon'], 1, 0, 0, 2)
snow = BigSister('snow', ['elsa', 'lane', 'kelly'], 1, 0, 0, 1)
belle = BigSister('belle', ['julia', 'betty', 'xena'], 0, 0, 0, 1)
carrie = BigSister('carrie', ['meg', 'pam', 'mara'], 1, 1, 0, 1)
miranda = BigSister('miranda', ['tara', 'hara', 'jana'], 0, 1, 0, 1)
samantha = BigSister('samantha', ['lane', 'mara', 'zenon'], 0, 1, 0, 1)
charlie = BigSister('charlie', ['julia', 'brenda', 'kelly'], 1, 1, 1, 2)
topanga = BigSister('topanga', ['julia', 'betty', 'xena'], 0, 1, 1, 1)
erica = BigSister('erica', ['meg', 'pam', 'barbie'], 0, 1, 1, 2)
jessica = BigSister('jessica', ['tara', 'hara', 'jana'], 0, 1, 1 , 1)
nicole = BigSister('nicole', ['lana', 'mara', 'zenon'], 0, 0, 2, 1)
lily = BigSister('lily', ['meg', 'pam', 'barbie'], 0, 0, 1, 2)
robin = BigSister('robin', ['serena', 'riley', 'maya'], 1, 0, 0, 0)
tracy = BigSister('tracy', ['elsa', 'brenda', 'kelly'], 0, 0, 0, 0)

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
big_sisters3 = [
    rhianna,
    molly,
    ariel,
    snow,
    belle,
    carrie,
    miranda,
    samantha,
    charlie,
    topanga,
    erica,
    jessica,
    nicole,
    lily,
    robin,
    tracy,
    ]

little_sisters0 = [ella, liz, sara]
little_sisters1 = [krista, marie, rowan]
little_sisters2 = [krista, marie, rowan, tina]

result0 = {bonnie : ella, anna : liz, laura : sara}
result1 = {emily : rowan, jess: marie, zoey : krista}
result2 = [
    rhianna,
    molly,
    ariel,
    snow,
    belle,
    carrie,
    miranda,
    samantha,
    ]
result3 = [
    rhianna,
    molly,
    ariel,
    snow,
    belle,
    carrie,
    miranda,
    samantha,
    charlie,
    erica,
    topanga,
    ]

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

    def test_get_big_sisters(self):
        self.assertEqual(get_big_sisters(big_sisters3, 8), (result2, None))
        self.assertEqual(get_big_sisters(big_sisters3, 11), (result3, None))


if __name__ == '__main__':
    unittest.main()