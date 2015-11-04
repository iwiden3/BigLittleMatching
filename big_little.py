#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import unittest
import big_little_tests
import Queue
from collections import defaultdict, deque

def matches(partners, proposers):
    result = {}
    proposers = deque(proposers)
    proposer_level = defaultdict(int)
    next_round = []
    while proposers:
        proposer = proposers.popleft()
        i = proposer_level[proposer['name']]
        if i < len(proposer['pref']):
            partner = [partner for partner in partners 
                       if partner['name'] == proposer['pref'][i]]
            if partner:
                match_found, removed_proposer = match(partner[0], proposer, result)
            else:
                match_found = False
            if match_found:
                if removed_proposer:
                    proposer_level[removed_proposer['name']] += 1
                    proposers.append(removed_proposer)
            else:
                proposer_level[proposer['name']] += 1
                proposers.append(proposer)
        else:
            next_round.append(proposer)

    return result, next_round


def match(partner, proposer, result):
    if partner['name'] not in result:
        result[partner['name']] = proposer
        return True, None
    current_proposer = result[partner['name']]
    if current_proposer['name'] in partner['pref']:
        current_proposer_rank = partner['pref'].index(current_proposer['name'])
    else:
        current_proposer_rank = len(partner['pref'])
    if proposer['name'] in partner['pref']:
        proposer_rank = partner['pref'].index(proposer['name'])
    else:
        proposer_rank = len(partner['pref'])
    if proposer_rank < current_proposer_rank:
        removed_partner = result[partner['name']]
        result[partner['name']] = proposer
        return True, removed_partner
    else:
        return False, None


def get_key(big):
    return big['want'] + big['dying_family'] - big['has_little']


def get_bigs(bigs, num):
    #if there are not enough big sisters for all the little sisters, error out
    bigs_with_twins = [big for big in bigs if big['twins'] == 1]
    if num > len(bigs_with_twins) + len(bigs):
        num = num - len(bigs_with_twins) - len(bigs)
        raise ValueError('Not enough bigs for all Littles, Need ' 
            + str(num) + ' more twins!')
    #big sisters who do not have a little sister and want one have the first priority
    first_round_bigs = [big for big in bigs if big['has_little'] == 0 and big['want'] > 0]
    if num <= len(first_round_bigs):
        return first_round_bigs, None
    #big sisters who want a little but have a little sister are second priority
    second_round_bigs = [big for big in bigs if big['want'] > 0 and big['has_little'] > 0]
    if num <= len(first_round_bigs) + len(second_round_bigs):
        second_round_bigs.sort(key=get_key, reverse=True)
        return first_round_bigs + second_round_bigs[:num - len(first_round_bigs)], None
    #if there are not enough bigs, try adding twins
    bigs_with_twins = [big for big in bigs if big['want'] > 0 and big['twins'] == 1]
    if num <= len(first_round_bigs) + len(second_round_bigs) + len(bigs_with_twins):
        bigs_with_twins.sort(key=get_key, reverse=True)
        num_bigs_with_twins = num - len(first_round_bigs) - len(second_round_bigs)
        return first_round_bigs + second_round_bigs, bigs_with_twins[:num_bigs_with_twins]
    #if there are not enough bigs with twins, and in last resort bigs
    third_round_bigs = [big for big in bigs if big['want'] == 0]
    if num <= len(bigs) + len(bigs_with_twins):
        number_last_bigs = len(bigs) + len(bigs_with_twins) - num
        third_round_bigs.sort(key=get_key, reverse=True)
        return first_round_bigs + second_round_bigs + third_round_bigs[:len(third_round_bigs)
         - number_last_bigs], bigs_with_twins
    return bigs, bigs_with_twins

def match_bigs_and_littles(bigs, littles):
    bigs, bigs_with_twins = get_bigs(bigs, len(littles))
    if bigs_with_twins:
        for big in bigs_with_twins:
            big_copy = copy.deepcopy(big)
            big_copy['name'] = big['name'] + '_copy'
            bigs.append(big_copy)
            for little in littles:
                if big['name'] in little['pref']:
                    ind = little['pref'].index(big['name']) + 1
                    little['pref'].insert(ind, big_copy['name'])

    #for round 1, littles have priority in choosing
    round1, littles = matches(bigs, littles)
    unmatched_bigs = [big for big in bigs if big['name'] not in round1.keys()]
    #for round 2, bigs have priority in choosing
    round2, bigs = matches(littles, unmatched_bigs)
    unmatched_littles = [little for little in littles if little['name'] not in round2.keys()]
    #for round 3, randomnly match bigs and littles
    result = {}
    if unmatched_littles:
        bigs.sort(key=get_key, reverse=True)
        priority_bigs = bigs[:len(unmatched_littles)]
        for i in range(len(priority_bigs)):
            pbig = priority_bigs[i]
            result[pbig['name']] = unmatched_littles[i]['name']

    #combine all results
    for k, v in round1.iteritems():
        result[k] = v['name']
    for k, v in round2.iteritems():
        result[v['name']] = k
    return result


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
        self.assertEqual(match_bigs_and_littles(bigs, littles), result)
        self.assertEqual(match_bigs_and_littles(big_little_tests.test_bigs1,
                         big_little_tests.test_littles1),
                         big_little_tests.test_result6)
        self.assertEqual(match_bigs_and_littles(big_little_tests.test_bigs1,
                         big_little_tests.test_littles2),
                         big_little_tests.test_result7)

        self.assertEqual(match_bigs_and_littles(big_little_tests.test_bigs1,
                         big_little_tests.test_littles3),
                         big_little_tests.test_result15)
        self.assertEqual(match_bigs_and_littles(copy.deepcopy(big_little_tests.bigs42),
                         copy.deepcopy(big_little_tests.littles42)),
                         big_little_tests.result42)
        self.assertEqual(match_bigs_and_littles(copy.deepcopy(big_little_tests.bigs52),
                         copy.deepcopy(big_little_tests.littles52)),
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

    def match(self):
        result = {}
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

    def test_get_bigs(self):
        self.assertEqual(get_bigs(big_little_tests.test_bigs1, 8),
                         (big_little_tests.test_result1, None))
        self.assertEqual(get_bigs(big_little_tests.test_bigs1, 11),
                         (big_little_tests.test_result2, None))
        self.assertEqual(get_bigs(big_little_tests.test_bigs1, 14),
                         (big_little_tests.test_result3, None))
        big_twins_result1 = [
            big_little_tests.big_carrie,
            big_little_tests.big_charlie,
            big_little_tests.big_miranda,
            big_little_tests.big_samantha,
            big_little_tests.big_erica,
            big_little_tests.big_topanga,
            big_little_tests.big_jessica,
            ]
        big_twins_result2 = [
            big_little_tests.big_carrie,
            big_little_tests.big_miranda,
            big_little_tests.big_samantha,
            big_little_tests.big_charlie,
            big_little_tests.big_topanga,
            big_little_tests.big_erica,
            big_little_tests.big_jessica,
            ]

        self.assertEqual(get_bigs(big_little_tests.test_bigs1, 21),
                         (big_little_tests.test_result4,
                         big_twins_result1))
        self.assertEqual(get_bigs(big_little_tests.test_bigs1, 23),
                         (big_little_tests.test_bigs1,
                         big_twins_result2))
        try:
            get_bigs(big_little_tests.test_bigs1, 24)
        except ValueError:
            pass
        except e:
            self.fail('Unexpecteed exception thrown', e)
        else:
            self.fail('ExpectedException not thrown')


if __name__ == '__main__':
    unittest.main()
