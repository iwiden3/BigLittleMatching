#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import unittest
import big_little_tests
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

	def get_rank(self, other):
		if other.name in self.pref:
			return self.pref.index(other.name)
		return None

class BigSister(Sister):
	def __init__(self, name, pref, dying_family, twins, has_little):
		super(BigSister, self).__init__(name, pref)
		self.dying_family = dying_family
		self.twins = twins
		self.has_little = has_little

	def __lt__(self, other):
		return self.get_score < other.get_score

	def get_score(big_sister):
    	#"""assign a priority to each big"""
		return self.want + self.dying_family - self.has_little

	def copy():
		return BigSister(self.name, copy.deepcopy(self.pref), self.dying_family, self.twins, self.has_little)

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
            partner = [partner for partner in partners if partner == proposer.pref[i]]
            if partner:
                (match_found, removed_proposer) = match(partner[0], proposer, result)
            else:
                match_found = False
            if match_found:
                if removed_proposer:
                    proposer_level[removed_proposer['name']] += 1
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

    third_round_bigs = [big for big in bigs if big['want'] == 0]
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
            big_sister_copy = big_sister.copy()
            big_sister_copy.name = big_sister.name + '_copy'
            big_sisters.append(big_sister_copy)
            for little_sister in little_sisters:
                ind = little_sister.get_rank(big_sister)
                if ind is not None:
                	little_sister.pref.insert(ind + 1, big_sister_copy.name)

    # for round 1, littles have priority in choosing
    (round1, little_sisters) = matches(big_sisters, little_sisters)
    unmatched_big_sisters = [big_sister for big_sister in big_sisters
                             if big_sister.name not in round1.keys()]

    # for round 2, bigs have priority in choosing

    (round2, big_sisters) = matches(little_sisters,
                                    unmatched_big_sisters)
    unmatched_little_sisters = [little_sister for little_sister in
                                little_sisters if little_sister.name
                                not in round2.keys()]

    # for round 3, arbitrarily match bigs and littles

    result = {}
    if unmatched_little_sisters:
        big_sisters.sort(reverse=True)
        priority_bigs = big_sisters[:len(unmatched_little_sisters)]
        for i in range(len(priority_bigs)):
            pbig = priority_bigs[i]
            result[pbig] = unmatched_little_sisters[i]

    # combine all results

    for (k, v) in round1.iteritems():
        result[k.name] = v.name
    for (k, v) in round2.iteritems():
       	result[v.name] = k.name
    return result
