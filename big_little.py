#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import unittest
import big_little_tests
import Queue as Q
from collections import defaultdict, deque

choices = 3


def matching(bigs, littles_original):
    littles = copy.deepcopy(littles_original)
    combined_result = {}
    (sorted_bigs, bigs_with_twins) = get_bigs(bigs, len(littles))
    bigs_dict = sisters_dict(sorted_bigs)
    if bigs_with_twins:
        for big_with_twin in bigs_with_twins:
            big_twin_name = big_with_twin['name'] + '_copy'
            big_twin_c = copy.deepcopy(big_with_twin)
            big_twin_c['name'] = big_twin_name
            bigs_dict[big_twin_name] = big_twin_c
            for little in littles:
                big_name = big_with_twin['name']
                if big_name in little['pref']:
                    ind = little['pref'].index(big_name) + 1
                    little['pref'].insert(ind, big_twin_name)

    (result, second_round_littles) = matches(bigs_dict, littles)
    littles_dict = sisters_dict(second_round_littles)
    unmatched_bigs = sisters_without_matches(bigs_dict, result)
    (result2, third_round_bigs) = matches(littles_dict, unmatched_bigs)
    unmatched_littles = sisters_without_matches(littles_dict, result2)
    if unmatched_littles:
        priority_bigs = sort_bigs(third_round_bigs)[:len(unmatched_littles)]
        for i in range(len(priority_bigs)):
            pbig = priority_bigs[i]
            pbig_name = pbig['name']
            combined_result[pbig_name] = unmatched_littles[i]['name']

    for (k, v) in result.iteritems():
        combined_result[k] = v['name']
    for (k, v) in result2.iteritems():
        combined_result[v['name']] = k
    #print combined_result
    return combined_result

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


def get_bigs(bigs, number_of_littles):
    
    bigs_twins = [big for big in bigs if big['twins'] == 1]
    if number_of_littles > (len(bigs_twins) + len(bigs)):
        num = number_of_littles - len(bigs_twins)-len(bigs)
        raise ValueError("Not enough bigs for all Littles, Need "+str(num)+" more twins!")


    first_bigs = [big for big in bigs if big['has_little'] == 0
                  and big['want'] > 0]
    # are there enough littles for the girls who have not been bigs and want a little?
    if number_of_littles <= len(first_bigs):
        return (first_bigs, None)
    
    second_bigs = [big for big in bigs if big['want'] > 0 and big['has_little'] > 0]
    if number_of_littles <= len(first_bigs) + len(second_bigs):
        num = len(first_bigs) + len(second_bigs) - number_of_littles
        s_bigs = sort_bigs(second_bigs)
        return (first_bigs + s_bigs[:len(s_bigs) - num], None)
    
    bigs_twins = [big for big in bigs if big['want'] > 0 and big['twins'] == 1]
    if number_of_littles <= len(first_bigs) + len(second_bigs) + len(bigs_twins):
        needed_twins = number_of_littles - len(first_bigs) - len(second_bigs)
        s_bigs_twins = sort_bigs(bigs_twins)
        return (first_bigs + second_bigs, s_bigs_twins[:needed_twins])
    last_bigs = [big for big in bigs if big['want'] == 0]
    if number_of_littles <= len(bigs) + len(bigs_twins):
        number_last_bigs = len(bigs) + len(bigs_twins ) - number_of_littles
        sorted_last_bigs = sort_bigs(last_bigs)
        a = first_bigs + second_bigs + sorted_last_bigs[:len(sorted_last_bigs) - number_last_bigs]
        return (first_bigs + second_bigs + sorted_last_bigs[:len(sorted_last_bigs) - number_last_bigs],bigs_twins)
    return (bigs, bigs_twins)

def get_twins(bigs, number_of_littles):
    needed_twins = number_of_littles - len(bigs)
    bigs_twins = [big for big in bigs if big['twins'] == 1]
    s_big_twins = sort_bigs(bigs_twins)
    return s_big_twins[:needed_twins]


class TestStringMethods(unittest.TestCase):

    def test_matching(self):
        bigs = [big_little_tests.big_emily, big_little_tests.big_jess,
                big_little_tests.big_zoey, big_little_tests.big_claire]
        littles = [big_little_tests.little_krista,
                   big_little_tests.little_marie,
                   big_little_tests.little_rowan,
                   big_little_tests.little_tina]
        result = {
            'emily': 'rowan',
            'jess': 'marie',
            'zoey': 'krista',
            'claire': 'tina',
            }
        self.assertEqual(matching(bigs, littles), result)
        self.assertEqual(matching(big_little_tests.test_bigs1,
                        big_little_tests.test_littles1),
                         big_little_tests.test_result6)
        self.assertEqual(matching(big_little_tests.test_bigs1,
                        big_little_tests.test_littles2),
                       big_little_tests.test_result7)

        self.assertEqual(matching(big_little_tests.test_bigs1,big_little_tests.test_littles3),big_little_tests.test_result15)
        self.assertEqual(matching(big_little_tests.bigs42,big_little_tests.littles42),big_little_tests.result42)

        self.assertEqual(matching(big_little_tests.bigs52,
                        big_little_tests.littles52),
                       big_little_tests.result52)

    def test_matches(self):
        self.assertEqual(matches(big_little_tests.bigs0,
                         big_little_tests.littles0),
                         (big_little_tests.result0, []))
        self.assertEqual(matches(big_little_tests.bigs1,
                         big_little_tests.littles1),
                         (big_little_tests.result1, []))
        self.assertEqual(matches(big_little_tests.bigs1,
                         big_little_tests.littles2),
                         (big_little_tests.result1,
                         [big_little_tests.little_tina]))
        self.assertEqual(matches(big_little_tests.bigs2,
                         big_little_tests.littles3),
                         (big_little_tests.result1,
                         [big_little_tests.little_tina]))

    def test_match(self):
        result = {}
        i = 0
        self.assertEqual(match(big_little_tests.bigs1,
                         big_little_tests.little_marie, 0, result),
                         (True, None))
        self.assertEqual(result['emily'], big_little_tests.little_marie)
        self.assertEqual(match(big_little_tests.bigs1,
                         big_little_tests.little_rowan, 0, result),
                         (True, big_little_tests.little_marie))
        self.assertEqual(result['emily'], big_little_tests.little_rowan)
        self.assertEqual(match(big_little_tests.bigs1,
                         big_little_tests.little_marie, 0, result),
                         (False, None))
        self.assertEqual(result['emily'], big_little_tests.little_rowan)

    def test_sister_without_matches(self):
        self.assertEqual(sisters_without_matches(big_little_tests.bigs2,
                         big_little_tests.result1),
                         [big_little_tests.big_claire])

    def test_sisters_dict(self):
        self.assertEqual(sisters_dict([big_little_tests.little_rowan]),
                         {'rowan': big_little_tests.little_rowan})

    def test_sort_bigs(self):
        bigs = [big_little_tests.big_emily, big_little_tests.big_zoey,
                big_little_tests.big_claire, big_little_tests.big_jess,
                big_little_tests.big_bonnie]
        self.assertEqual(sort_bigs(bigs), bigs)

    def test_get_bigs(self):
        self.assertEqual(get_bigs(big_little_tests.test_bigs1, 8),
                         (big_little_tests.test_result1, None))
        self.assertEqual(get_bigs(big_little_tests.test_bigs1, 11),
                         (big_little_tests.test_result2, None))
        self.assertEqual(get_bigs(big_little_tests.test_bigs1, 14),
                         (big_little_tests.test_result3, None))
        big_twins_result1 = [big_little_tests.big_carrie,big_little_tests.big_charlie,big_little_tests.big_miranda,big_little_tests.big_samantha,big_little_tests.big_erica,big_little_tests.big_topanga,big_little_tests.big_jessica]
        big_twins_result2 = [big_little_tests.big_carrie,big_little_tests.big_miranda,big_little_tests.big_samantha,big_little_tests.big_charlie,big_little_tests.big_topanga,big_little_tests.big_erica,big_little_tests.big_jessica]

        self.assertEqual(get_bigs(big_little_tests.test_bigs1, 21),(big_little_tests.test_result4, big_twins_result1))
        self.assertEqual(get_bigs(big_little_tests.test_bigs1, 23),
                         (big_little_tests.test_bigs1, big_twins_result2))
        try:
            get_bigs(big_little_tests.test_bigs1, 24)
        except ValueError:
            pass
        except e:
            self.fail("Unexpecteed exception thrown",e)
        else:
            self.fail("ExpectedException not thrown")


if __name__ == '__main__':
    unittest.main()
