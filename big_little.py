#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import unittest
import big_little_tests
import xlrd
from collections import defaultdict, deque


def matches(partners, proposers):
    """find a stable match between the partners and the proposers"""

    result = {}
    proposers = deque(proposers)
    proposer_level = defaultdict(int)
    next_round = []
    while proposers:
        proposer = proposers.popleft()
        i = proposer_level[proposer['name']]
        if i < len(proposer['pref']):
            partner = [partner for partner in partners if partner['name'] == proposer['pref'][i]]
            if partner:
                (match_found, removed_proposer) = match(partner[0], proposer, result)
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

    return (result, next_round)


def match(partner, proposer, result):
    """check and see if the proposer is the best match for the partner"""

    if partner['name'] not in result:
        result[partner['name']] = proposer
        return (True, None)
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
        return (True, removed_partner)
    else:
        return (False, None)


def excel_to_dictionary(filename):
    """create dictionary from excel"""

    book = xlrd.open_workbook(filename)
    first_sheet = book.sheet_by_index(0)
    col_names = first_sheet.row_values(0)
    dict_list = []
    for row_index in xrange(1, first_sheet.nrows):
        d = {'pref': []}
        for col_index in xrange(0, first_sheet.ncols):
            if col_names[col_index].startswith('pref'):
                d['pref'].append(first_sheet.cell(row_index, col_index).value)
            else:
                d[col_names[col_index]] = first_sheet.cell(row_index, col_index).value
        dict_list.append(d)
    return dict_list


def get_key(big_sister):
    """assign a priority to each big"""

    return big_sister['want'] + big_sister['dying_family'] - big_sister['has_little']


def get_big_sisters(bigs, num):
    """decide who will be bigs based on the number of littles """

    # if there are not enough big sisters for all the little sisters, error out

    bigs_with_twins = [big for big in bigs if big['twins'] == 1]
    if num > len(bigs_with_twins) + len(bigs):
        num = num - len(bigs_with_twins) - len(bigs)
        raise ValueError('Not enough bigs for all Littles, Need '
                         + str(num) + ' more twins!')

    # big sisters who do not have a little sister and want one have the first priority

    first_round_bigs = [big for big in bigs if big['has_little'] == 0
                        and big['want'] > 0]
    if num <= len(first_round_bigs):
        return (first_round_bigs, None)

    # big sisters who want a little but have a little sister are second priority

    second_round_bigs = [big for big in bigs if big['want'] > 0
                         and big['has_little'] > 0]
    if num <= len(first_round_bigs) + len(second_round_bigs):
        second_round_bigs.sort(key=get_key, reverse=True)
        return (first_round_bigs + second_round_bigs[:num
                - len(first_round_bigs)], None)

    # if there are not enough bigs, try adding twins

    bigs_with_twins = [big for big in bigs if big['want'] > 0
                       and big['twins'] == 1]
    if num <= len(first_round_bigs) + len(second_round_bigs) + len(bigs_with_twins):
        bigs_with_twins.sort(key=get_key, reverse=True)
        num_bigs_with_twins = num - len(first_round_bigs) - len(second_round_bigs)
        return (first_round_bigs + second_round_bigs, bigs_with_twins[:num_bigs_with_twins])

    # if there are not enough bigs with twins, and in last resort bigs

    third_round_bigs = [big for big in bigs if big['want'] == 0]
    if num <= len(bigs) + len(bigs_with_twins):
        number_last_bigs = len(bigs) + len(bigs_with_twins) - num
        third_round_bigs.sort(key=get_key, reverse=True)
        return (first_round_bigs + second_round_bigs
                + third_round_bigs[:len(third_round_bigs)
                - number_last_bigs], bigs_with_twins)
    return (bigs, bigs_with_twins)


def match_sisters(big_sisters, little_sisters):
    """match bigs with littles so that the matching is stable"""

    (big_sisters, bigs_with_twins) = get_big_sisters(big_sisters,
            len(little_sisters))
    if bigs_with_twins:
        for big_sister in bigs_with_twins:
            big_sister_copy = copy.deepcopy(big_sister)
            big_sister_copy['name'] = big_sister['name'] + '_copy'
            big_sisters.append(big_sister_copy)
            for little_sister in little_sisters:
                if big_sister['name'] in little_sister['pref']:
                    ind = little_sister['pref'].index(big_sister['name'
                            ]) + 1
                    little_sister['pref'].insert(ind,
                            big_sister_copy['name'])

    # for round 1, littles have priority in choosing

    (round1, little_sisters) = matches(big_sisters, little_sisters)
    unmatched_big_sisters = [big_sister for big_sister in big_sisters
                             if big_sister['name'] not in round1.keys()]

    # for round 2, bigs have priority in choosing

    (round2, big_sisters) = matches(little_sisters,
                                    unmatched_big_sisters)
    unmatched_little_sisters = [little_sister for little_sister in
                                little_sisters if little_sister['name']
                                not in round2.keys()]

    # for round 3, arbitrarily match bigs and littles

    result = {}
    if unmatched_little_sisters:
        big_sisters.sort(key=get_key, reverse=True)
        priority_bigs = big_sisters[:len(unmatched_little_sisters)]
        for i in range(len(priority_bigs)):
            pbig = priority_bigs[i]
            result[pbig['name']] = unmatched_little_sisters[i]['name']

    # combine all results

    for (k, v) in round1.iteritems():
        result[k] = v['name']
    for (k, v) in round2.iteritems():
        result[v['name']] = k
    return result


class TestStringMethods(unittest.TestCase):

    def test_matches(self):
        self.assertEqual(matches(big_little_tests.big_sisters0,
                         big_little_tests.little_sisters0),
                         (big_little_tests.result0, []))
        self.assertEqual(matches(big_little_tests.big_sisters1,
                         big_little_tests.little_sisters1),
                         (big_little_tests.result1, []))
        self.assertEqual(matches(big_little_tests.big_sisters1,
                         big_little_tests.little_sisters2),
                         (big_little_tests.result1,
                         [big_little_tests.little_tina]))
        self.assertEqual(matches(big_little_tests.big_sisters2,
                         big_little_tests.little_sisters2),
                         (big_little_tests.result1,
                         [big_little_tests.little_tina]))

    def test_match_sisters(self):
        self.assertEqual(match_sisters(big_little_tests.big_sisters2,
                         big_little_tests.little_sisters2),
                         big_little_tests.result2)
        self.assertEqual(match_sisters(big_little_tests.big_sisters3,
                         big_little_tests.little_sisters3),
                         big_little_tests.result3)
        self.assertEqual(match_sisters(big_little_tests.big_sisters3,
                         big_little_tests.little_sisters4),
                         big_little_tests.result4)

        self.assertEqual(match_sisters(big_little_tests.big_sisters3,
                         big_little_tests.little_sisters5),
                         big_little_tests.result5)
        self.assertEqual(match_sisters(copy.deepcopy(big_little_tests.big_sisters4),
                         copy.deepcopy(big_little_tests.little_sisters6)),
                         big_little_tests.result6)
        self.assertEqual(match_sisters(copy.deepcopy(big_little_tests.big_sisters5),
                         copy.deepcopy(big_little_tests.little_sisters7)),
                         big_little_tests.result7)

    def test_match(self):
        result = {}
        self.assertEqual(match(big_little_tests.big_emily,
                         big_little_tests.little_marie, result), (True,
                         None))
        self.assertEqual(result['emily'], big_little_tests.little_marie)
        self.assertEqual(match(big_little_tests.big_emily,
                         big_little_tests.little_rowan, result), (True,
                         big_little_tests.little_marie))
        self.assertEqual(result['emily'], big_little_tests.little_rowan)
        self.assertEqual(match(big_little_tests.big_emily,
                         big_little_tests.little_marie, result),
                         (False, None))
        self.assertEqual(result['emily'], big_little_tests.little_rowan)

    def test_get_big_sisters(self):
        self.assertEqual(get_big_sisters(big_little_tests.big_sisters3,
                         8), (big_little_tests.result8, None))
        self.assertEqual(get_big_sisters(big_little_tests.big_sisters3,
                         11), (big_little_tests.result9, None))
        self.assertEqual(get_big_sisters(big_little_tests.big_sisters3,
                         14), (big_little_tests.result10, None))
        self.assertEqual(get_big_sisters(big_little_tests.big_sisters3,
                         21), (big_little_tests.result11,
                         big_little_tests.result12))
        self.assertEqual(get_big_sisters(big_little_tests.big_sisters3,
                         23), (big_little_tests.big_sisters3,
                         big_little_tests.result13))
        try:
            get_big_sisters(big_little_tests.big_sisters3, 24)
        except ValueError:
            pass
        except e:
            self.fail('Unexpecteed exception thrown', e)
        else:
            self.fail('ExpectedException not thrown')


if __name__ == '__main__':
    unittest.main()

    # filename1 = raw_input("Input Excel data for bigs: ")
    # filename2 = raw_input("Input Excel data for littles: ")
    # try:
     #   big_sisters = excel_to_dictionary(filename1)
      #  little_sisters = excel_to_dictionary(filename2)
       # print match_sisters(big_sisters, little_sisters)
    # except IOError:
     #   print "Check filenames!"
