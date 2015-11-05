#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import xlrd
from collections import defaultdict, deque

class Sister(object):
	def __init__(self, name, pref):
		self.name = name
		self.pref = pref

	def __eq__(self, other):
		return self.name == other.name

	def __hash__(self):
		return hash(self.name)

	def __repr__(self):
		return self.name

	def get_rank(self, other):
		if other.name in self.pref:
			return self.pref.index(other.name)
		return None

class BigSister(Sister):
	def __init__(self, name, pref, dying_family, twins, has_little, want):
		super(BigSister, self).__init__(name, pref)
		self.dying_family = dying_family
		self.twins = twins
		self.has_little = has_little
		self.want = want

	def __lt__(self, other):
		return self.get_score() < other.get_score()

	def get_score(self):
    #"""assign a priority to each big"""
		return self.want + self.dying_family - self.has_little

class LittleSister(Sister):
	pass


def matches(partners, proposers):
    """find a stable match between the partners and the proposers"""

    result = {}
    proposers = deque(proposers)
    proposer_level = defaultdict(int)
    next_round = []
    while proposers:
        proposer = proposers.popleft()
        i = proposer_level[proposer]
        if i < len(proposer.pref):
            partner = [partner for partner in partners if partner.name == proposer.pref[i]]
            if partner:
                (match_found, removed_proposer) = match(partner[0], proposer, result)
            else:
                match_found = False
            if match_found:
                if removed_proposer:
                    proposer_level[removed_proposer] += 1
                    proposers.append(removed_proposer)
            else:
                proposer_level[proposer] += 1
                proposers.append(proposer)
        else:
            next_round.append(proposer)

    return (result, next_round)

def match(partner, proposer, result):
    """check and see if the proposer is the best match for the partner"""
    if partner not in result:
        result[partner] = proposer
        return (True, None)
    current_proposer = result[partner]
    proposer_rank = partner.get_rank(proposer)
    current_proposer_rank = partner.get_rank(current_proposer)
    if proposer_rank is not None and current_proposer_rank is not None:
    	if proposer_rank < current_proposer_rank:
    		result[partner] = proposer
    		return (True, current_proposer)
    return (False, None)

def excel_to_dictionary(filename):
    """create dictionary from excel"""

    book = xlrd.open_workbook(filename)
    first_sheet = book.sheet_by_index(0)
    col_names = first_sheet.row_values(0)
    result = []
    for row_index in xrange(1, first_sheet.nrows):
        d = {'pref': []}
        for col_index in xrange(0, first_sheet.ncols):
            if col_names[col_index].startswith('pref'):
                d['pref'].append(first_sheet.cell(row_index, col_index).value)
            else:
                d[col_names[col_index]] = first_sheet.cell(row_index, col_index).value
        result.append(d)
    return result

def read_sisters(l, f):
    result = []
    for d in l:
        if f == "BigSister":
            sister = BigSister(d['name'], d['pref'], d['dying_family'], d['twins'], d['has_little'], d['want'])
        elif f == "LittleSister":
            sister = LittleSister(d['name'], d['pref'])
        result.append(sister)
    return result

def get_big_sisters(bigs, num):
    """decide who will be bigs based on the number of littles """

    # if there are not enough big sisters for all the little sisters, error out

    bigs_with_twins = [big for big in bigs if big.twins == 1]
    if num > len(bigs_with_twins) + len(bigs):
        num = num - len(bigs_with_twins) - len(bigs)
        raise ValueError('Not enough bigs for all Littles, Need '
                         + str(num) + ' more twins!')

    # big sisters who do not have a little sister and want one have the first priority

    first_round_bigs = [big for big in bigs if big.has_little == 0
                        and big.want > 0]
    if num <= len(first_round_bigs):
        return (first_round_bigs, None)

    # big sisters who want a little but have a little sister are second priority

    second_round_bigs = [big for big in bigs if big.want > 0
                         and big.has_little > 0]
    if num <= len(first_round_bigs) + len(second_round_bigs):
        second_round_bigs.sort(reverse=True)
        return (first_round_bigs + second_round_bigs[:num
                - len(first_round_bigs)], None)

    # if there are not enough bigs, try adding twins

    bigs_with_twins = [big for big in bigs if big.want > 0
                       and big.twins == 1]
    if num <= len(first_round_bigs) + len(second_round_bigs) + len(bigs_with_twins):
        bigs_with_twins.sort(reverse=True)
        num_bigs_with_twins = num - len(first_round_bigs) - len(second_round_bigs)
        return (first_round_bigs + second_round_bigs, bigs_with_twins[:num_bigs_with_twins])

    # if there are not enough bigs with twins, and in last resort bigs

    third_round_bigs = [big for big in bigs if big.want == 0]
    if num <= len(bigs) + len(bigs_with_twins):
        number_last_bigs = len(bigs) + len(bigs_with_twins) - num
        third_round_bigs.sort(reverse=True)
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
            big_sister_copy.name = big_sister.name + '_copy'
            big_sisters.append(big_sister_copy)
            for little_sister in little_sisters:
                ind = little_sister.get_rank(big_sister)
                if ind is not None:
                	little_sister.pref.insert(ind + 1, big_sister_copy.name)

    # for round 1, littles have priority in choosing
    (round1, little_sisters) = matches(big_sisters, little_sisters)
    unmatched_big_sisters = [big_sister for big_sister in big_sisters
                             if big_sister not in round1.keys()]

    # for round 2, bigs have priority in choosing
    (round2, big_sisters) = matches(little_sisters,
                                    unmatched_big_sisters)
    unmatched_little_sisters = [little_sister for little_sister in
                                little_sisters if little_sister
                                not in round2.keys()]

    # for round 3, arbitrarily match bigs and littles
    result = {}
    if unmatched_little_sisters:
        big_sisters.sort(reverse=True)
        priority_bigs = big_sisters[:len(unmatched_little_sisters)]
        for i in range(len(priority_bigs)):
            pbig = priority_bigs[i]
            result[pbig.name] = unmatched_little_sisters[i].name

    # combine all results
    for (k, v) in round1.iteritems():
        result[k.name] = v.name
    for (k, v) in round2.iteritems():
       	result[v.name] = k.name
    return result

if __name__ == '__main__':
    filename1 = raw_input("Input Excel data for bigs: ")
    filename2 = raw_input("Input Excel data for littles: ")
    try:
        big_sisters = read_sisters(excel_to_dictionary(filename1), "BigSister")
        little_sisters = read_sisters(excel_to_dictionary(filename2), "LittleSister")
        print match_sisters(big_sisters, little_sisters)
    except IOError:
        print "Check filenames!"
