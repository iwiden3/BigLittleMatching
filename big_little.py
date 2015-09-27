#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import unittest
import big_little_tests
import Queue as Q
from collections import defaultdict, deque

choices = 3

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
        self.assertEqual(get_bigs(big_little_tests.test_bigs1,7),(big_little_tests.test_result1, False))
        self.assertEqual(get_bigs(big_little_tests.test_bigs1,11),(big_little_tests.test_result2,False))
        self.assertEqual(get_bigs(big_little_tests.test_bigs1,14),(big_little_tests.test_result3,False))
        self.assertEqual(get_bigs(big_little_tests.test_bigs1,21),(big_little_tests.test_result4,True))
        self.assertEqual(get_bigs(big_little_tests.test_bigs1,24),(big_little_tests.test_bigs1,True))
        self.assertEqual(get_bigs(big_little_tests.test_bigs1,22),(big_little_tests.test_result5,True))

    def test_sort_bigs(self):
        bigs20 = [big_little_tests.big_emily, big_little_tests.big_zoey, big_little_tests.big_claire, big_little_tests.big_jess,big_little_tests.big_bonnie]
        self.assertEqual(sort_bigs(bigs20), bigs20)

    def test_matching(self):
        bigs20 = [big_little_tests.big_emily,big_little_tests.big_jess,big_little_tests.big_zoey,big_little_tests.big_claire]
        littles30 = [big_little_tests.little_krista, big_little_tests.little_marie, big_little_tests.little_rowan,
                     big_little_tests.little_tina]
        result50 = {
            'emily': 'rowan',
            'jess': 'marie',
            'zoey': 'krista',
            'claire': 'tina',
            }
        self.assertEqual(matching(bigs20, littles30), result50)
        self.assertEqual(matching(big_little_tests.test_bigs1,big_little_tests.test_littles1), big_little_tests.test_result6)
        self.assertEqual(matching(big_little_tests.test_bigs1,big_little_tests.test_littles2), big_little_tests.test_result7)
       # self.assertEqual(matching(test_bigs1,test_littles3),test_result7)
        #self.assertEqual(matching(big_little_tests.bigs42,big_little_tests.littles42),big_little_tests.result42)
        self.assertEqual(matching(big_little_tests.bigs52,big_little_tests.littles52),big_little_tests.result52)

    def matches_second_round(self):
        result11 = {'tina': big_little_tests.big_claire}
        self.assertEqual(matches_second_round(bigs2, [big_little_tests.little_tina],
                         result1), (result11, []))

    def test_match(self):
        result = {}
        i = 0
        self.assertEqual(match(big_little_tests.bigs1, big_little_tests.little_marie, 0, result), (True,
                         None))
        self.assertEqual(result['emily'], big_little_tests.little_marie)
        self.assertEqual(match(big_little_tests.bigs1, big_little_tests.little_rowan, 0, result), (True,
                         big_little_tests.little_marie))
        self.assertEqual(result['emily'], big_little_tests.little_rowan)
        self.assertEqual(match(big_little_tests.bigs1, big_little_tests.little_marie, 0, result), (False,
                         None))
        self.assertEqual(result['emily'], big_little_tests.little_rowan)

    def match_second_round(self):
        result = {}
        i = 0
        littles5 = [big_little_tests.little_rowan, little_marie, little_krista]
        l1 = sisters_dict(littles5)
        self.assertEqual(match_second_round(big_little_tests.big_jess, l1, i, result),
                         (True, None))
        self.assertEqual(result['rowan'], big_jess)
        self.assertEqual(match_second_round(big_little_tests.big_emily, l1, i, result),
                         (True, big_jess))
        self.assertEqual(result['rowan'], big_emily)
        self.assertEqual(match_second_round(big_little_tests.big_jess, l1, i, result),
                         (False, None))
        self.assertEqual(result['rowan'], big_little_tests.big_emily)

    def test_matches(self):
        self.assertEqual(matches(big_little_tests.bigs0, big_little_tests.littles0), (big_little_tests.result0, []))
        self.assertEqual(matches(big_little_tests.bigs1, big_little_tests.littles1), (big_little_tests.result1, []))
        self.assertEqual(matches(big_little_tests.bigs1, big_little_tests.littles2), (big_little_tests.result1,
                         [big_little_tests.little_tina]))
        self.assertEqual(matches(big_little_tests.bigs2, big_little_tests.littles3), (big_little_tests.result1,
                         [big_little_tests.little_tina]))

    def test_sisters_dict(self):
        self.assertEqual(sisters_dict([big_little_tests.little_rowan]),
                         {'rowan': big_little_tests.little_rowan})

    def test_sister_without_matches(self):
        self.assertEqual(sisters_without_matches(big_little_tests.bigs2, big_little_tests.result1),
                         [big_little_tests.big_claire])


if __name__ == '__main__':
    unittest.main()
