#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import unittest
import big_little_tests
import Queue as Q
from collections import defaultdict, deque
from big_little_tests import test_bigs1,test_result1,test_result2,test_result3,test_result4,test_result5,test_result6,test_littles1,test_result7,test_littles2,test_littles3,test_twins_bigs1,test_twins_littles1
choices = 3
big_anna = {
    'name': 'anna',
    'want': 2,
    'twins': 0,
    'pref': ['ella', 'liz', 'sara'],
    'has_little': 0,

    }
big_laura = {
    'name': 'laura',
    'want': 2,
    'twins': 0,
    'pref': ['sara', 'ella', 'liz'],
    'has_little': 0,

    }
big_bonnie = {
    'name': 'bonnie',
    'want': 0,
    'twins': 0,
    'pref': ['liz', 'ella', 'sara'],
    'dying_family': 0,
    'has_little': 3,

    }
bigs0 = {'anna': big_anna, 'laura': big_laura, 'bonnie': big_bonnie}

little_ella = {'name': 'ella', 'pref': ['bonnie', 'laura', 'anna']}
little_liz = {'name': 'liz', 'pref': ['anna', 'bonnie', 'laura']}
little_sara = {'name': 'sara', 'pref': ['laura', 'anna', 'bonnie']}
littles0 = [little_ella, little_liz, little_sara]
result0 = {'bonnie': little_ella, 'anna': little_liz,
           'laura': little_sara}
result5 = {'ella': big_anna, 'liz': big_bonnie, 'sara': big_laura}

big_emily = {
    'name': 'emily',
    'want': 2,
    'twins': 0,
    'pref': ['rowan', 'marie', 'krista'],
    'dying_family': 1,
    'has_little': 0,
    }
big_jess = {
    'name': 'jess',
    'want': 2,
    'twins': 0,
    'pref': ['rowan', 'krista', 'marie'],
    'dying_family': 0,
    'has_little': 1,
    }
big_zoey = {
    'name': 'zoey',
    'want': 2,
    'twins': 0,
    'pref': ['marie', 'rowan', 'krista'],
    'dying_family': 1,
    'has_little': 2,
    }
big_claire = {
    'name': 'claire',
    'want': 2,
    'twins': 0,
    'pref': ['marie', 'rowan', 'tina'],
    'dying_family': 0,
    'has_little': 3,
    }

bigs1 = {'emily': big_emily, 'jess': big_jess, 'zoey': big_zoey}
bigs2 = {
    'emily': big_emily,
    'jess': big_jess,
    'zoey': big_zoey,
    'claire': big_claire,
    }

little_krista = {'name': 'krista', 'pref': ['zoey', 'emily', 'jess']}
little_marie = {'name': 'marie', 'pref': ['emily', 'jess', 'zoey']}
little_rowan = {'name': 'rowan', 'pref': ['emily', 'jess', 'zoey']}
little_tina = {'name': 'tina', 'pref': ['emily', 'jess', 'zoey']}

littles1 = [little_krista, little_marie, little_rowan]
littles2 = [little_krista, little_marie, little_rowan, little_tina]
littles3 = [little_krista, little_marie, little_rowan, little_tina]

result1 = {'emily': little_rowan, 'jess': little_marie,
           'zoey': little_krista}

def matching(bigs, littles):
    combined_result = {}
    sorted_bigs,is_twins = get_bigs(bigs,len(littles))
    bigs_dict = sisters_dict(sorted_bigs)
    if is_twins:
        bigs_with_twins = get_twins(bigs,len(littles))
        for big_with_twin in bigs_with_twins:
            big_twin_name = big_with_twin['name'] + "_copy"
            big_twin_c = copy.deepcopy(big_with_twin)
            big_twin_c['name'] = big_twin_name
            bigs_dict[big_twin_name] = big_twin_c
            for little in littles:
                big_name = big_with_twin['name']
                if big_name in little['pref']:
                    ind = little['pref'].index(big_name) + 1
                    little['pref'].insert(ind,big_twin_name)


    (result, second_round) = matches(bigs_dict, littles)
    littles_dict = sisters_dict(second_round)
    unmatched_bigs = sisters_without_matches(bigs_dict, result)
    (result2, third_round) = matches(littles_dict,unmatched_bigs)
    unmatched_littles = sisters_without_matches(littles_dict,result2)
    if unmatched_littles:
        priority_bigs = sort_bigs(third_round)[:len(unmatched_littles)]
        for i in range(len(priority_bigs)):
            pbig = priority_bigs[i]
            k = pbig['name']
            combined_result[k] = unmatched_littles[i]['name']

    for (k, v) in result.iteritems():
        combined_result[k] = v['name']
    for (k, v) in result2.iteritems():
        combined_result[v['name']] = k
    #print combined_result
    return combined_result
 
def get_twins(bigs,number_of_littles):
    needed_twins = number_of_littles - len(bigs)
    bigs_twins = [big for big in bigs if big['twins'] == 1]
    s_big_twins = sort_bigs(bigs_twins)
    return s_big_twins[:needed_twins]

def matches(bigs, littles):
    result = {}
    littles = deque(littles)
    little_level = defaultdict(int)
    second_round = []
    while littles:
        little = littles.popleft()
        i = little_level[little['name']]
        if i < choices:
            (match_found, removed_little) = match(bigs, little, i,
                    result)
            if match_found:
                if removed_little:
                    little_level[removed_little['name']] += 1
                    littles.append(removed_little)
            else:
                little_level[little['name']] += 1
                littles.append(little)
        else:
            second_round.append(little)

    return (result, second_round)

def match(
    bigs,
    little,
    i,
    result,
    ):

    big_name = little['pref'][i]
    if big_name not in result and big_name in bigs.keys():
        result[big_name] = little
        return (True, None)
    elif big_name in bigs.keys():
        curr_little = result[big_name]['name']
        temp_little = little['name']
        curr_big_ranks = bigs[big_name]['pref']
        curr_little_rank = choices + 1
        if curr_little in curr_big_ranks:
            curr_little_rank = curr_big_ranks.index(curr_little) + 1
        temp_little_rank = choices + 1
        if temp_little in curr_big_ranks:
            temp_little_rank = curr_big_ranks.index(temp_little) + 1
        if temp_little_rank < curr_little_rank:
            removed_little = result[big_name]
            result[big_name] = little
            return (True, removed_little)
        else:
            return (False, None)
    else:
        return (False, None)


def sisters_without_matches(sisters, result):
    all_sisters = set(sisters.keys())
    matched_sisters = set(result.keys())
    unmatched_sisters = all_sisters ^ matched_sisters
    return [sisters[sister] for sister in unmatched_sisters]


def sisters_dict(sisters):
    d = {}
    for sister in sisters:
        d[sister['name']] = sister
    return d


def sort_bigs(bigs):
    bigs.sort(key=get_key, reverse=True)
    return bigs


def get_key(big):
    return big['want'] + big['dying_family'] - big['has_little']

def get_bigs(bigs,number_of_littles):
    first_bigs = [big for big in bigs if big['has_little'] == 0 and big['want'] > 0]
    #are there enough littles for the girls who have not been bigs and want a little?
    if number_of_littles <= len(first_bigs):
        return (first_bigs, False)
    second_bigs = [big for big in bigs if big['want'] > 0 and big['has_little'] > 0] 
    if number_of_littles <= (len(first_bigs) + len(second_bigs)):
        num = (len(first_bigs) + len(second_bigs)) - number_of_littles
        s_bigs = sort_bigs(second_bigs)
        return (first_bigs + s_bigs[:(len(s_bigs)-num)],False)
    third_bigs = [big for big in bigs if big['want'] > 0 and big['twins'] == 1]
    if number_of_littles <= (len(first_bigs) + len(second_bigs) + len(third_bigs)):
        return (first_bigs + second_bigs,True)
    fourth_bigs = [big for big in bigs if big['want'] == 0]
    if number_of_littles <= (len(bigs)+len(third_bigs)):
        num = len(bigs) + len(third_bigs) - number_of_littles
        s_bigs = sort_bigs(fourth_bigs)
        return (first_bigs + second_bigs + s_bigs[:(len(s_bigs) - num)],True)
    return (bigs,True)



class TestStringMethods(unittest.TestCase):

    def match_twins_priority(self):
        big_miranda = {'name': 'miranda','want': 1,'twins': 1,'pref': ['tara', 'hara', 'jana'],'dying_family': 0,'has_little': 0}
        little_tara = {'name': 'tara', 'pref': ['molly', 'ariel', 'snow']}
        g = match_twins_priority(test_twins_littles1,test_twins_bigs1)
        score,b,l = g.get()
        self.assertEqual((b,l),(big_miranda,little_tara))

    def test_get_bigs(self):
        self.assertEqual(get_bigs(test_bigs1,7),(test_result1, False))
        self.assertEqual(get_bigs(test_bigs1,11),(test_result2,False))
        self.assertEqual(get_bigs(test_bigs1,14),(test_result3,False))
        self.assertEqual(get_bigs(test_bigs1,21),(test_result4,True))
        self.assertEqual(get_bigs(test_bigs1,24),(test_bigs1,True))
        self.assertEqual(get_bigs(test_bigs1,22),(test_result5,True))

    def test_sort_bigs(self):
        bigs20 = [big_emily, big_zoey, big_claire, big_jess,big_bonnie]
        self.assertEqual(sort_bigs(bigs20), bigs20)

    def test_matching(self):
        bigs20 = [big_emily,big_jess,big_zoey,big_claire]
        littles30 = [little_krista, little_marie, little_rowan,
                     little_tina]
        result50 = {
            'emily': 'rowan',
            'jess': 'marie',
            'zoey': 'krista',
            'claire': 'tina',
            }
        self.assertEqual(matching(bigs20, littles30), result50)
        self.assertEqual(matching(test_bigs1,test_littles1), test_result6)
        self.assertEqual(matching(test_bigs1,test_littles2), test_result7)
       # self.assertEqual(matching(test_bigs1,test_littles3),test_result7)
        #self.assertEqual(matching(big_little_tests.bigs42,big_little_tests.littles42),big_little_tests.result42)
        self.assertEqual(matching(big_little_tests.bigs52,big_little_tests.littles52),big_little_tests.result52)

    def matches_second_round(self):
        result11 = {'tina': big_claire}
        self.assertEqual(matches_second_round(bigs2, [little_tina],
                         result1), (result11, []))

    def test_match(self):
        result = {}
        i = 0
        self.assertEqual(match(bigs1, little_marie, 0, result), (True,
                         None))
        self.assertEqual(result['emily'], little_marie)
        self.assertEqual(match(bigs1, little_rowan, 0, result), (True,
                         little_marie))
        self.assertEqual(result['emily'], little_rowan)
        self.assertEqual(match(bigs1, little_marie, 0, result), (False,
                         None))
        self.assertEqual(result['emily'], little_rowan)

    def match_second_round(self):
        result = {}
        i = 0
        littles5 = [little_rowan, little_marie, little_krista]
        l1 = sisters_dict(littles5)
        self.assertEqual(match_second_round(big_jess, l1, i, result),
                         (True, None))
        self.assertEqual(result['rowan'], big_jess)
        self.assertEqual(match_second_round(big_emily, l1, i, result),
                         (True, big_jess))
        self.assertEqual(result['rowan'], big_emily)
        self.assertEqual(match_second_round(big_jess, l1, i, result),
                         (False, None))
        self.assertEqual(result['rowan'], big_emily)

    def test_matches(self):
        self.assertEqual(matches(bigs0, littles0), (result0, []))
        self.assertEqual(matches(bigs1, littles1), (result1, []))
        self.assertEqual(matches(bigs1, littles2), (result1,
                         [little_tina]))
        self.assertEqual(matches(bigs2, littles3), (result1,
                         [little_tina]))

    def test_sisters_dict(self):
        self.assertEqual(sisters_dict([little_rowan]),
                         {'rowan': little_rowan})

    def test_sister_without_matches(self):
        self.assertEqual(sisters_without_matches(bigs2, result1),
                         [big_claire])


if __name__ == '__main__':
    unittest.main()
