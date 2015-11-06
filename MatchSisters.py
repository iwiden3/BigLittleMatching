#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import xlrd
from collections import defaultdict, deque

BIG_SISTER = "Big Sister"
LITTLE_SISTER = "Little Sister"

class Sister(object):

    def __init__(self, name, pref):
        """
        Args:
            name (string): Name of Sister.
            pref (list): List of names of Sisters. 
        """
        self.name = name
        self.pref = pref

    def __eq__(self, other):
        if not isinstance(other, Sister):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def get_rank(self, other):
        """Get rank of other sister in preference list, defaulting to None."""
        if other.name in self.pref:
            return self.pref.index(other.name)
        return None

class BigSister(Sister):

    def __init__(self, name, pref, has_dying_family,
                 wants_twins, num_littles, want_level):
        super(BigSister, self).__init__(name, pref)
        self.has_dying_family = bool(has_dying_family)
        self.wants_twins = bool(wants_twins)
        self.num_littles = num_littles
        self.want_level = want_level

    def __lt__(self, other):
       return self.get_score() < other.get_score()

    def get_score(self):
        """Compute a general priority for this big."""
        return self.want_level + int(self.has_dying_family) - self.num_littles

class LittleSister(Sister):
    pass


def matches(partners, proposers):
    """Find a stable match between the partners and the proposers.
    
    Args:
        partners (list): List of sisters. 
        proposers (list): List of sisters.
    
    Returns:
        dict: The mapping between big sister names and little sister names.
    """

    result = {}
    proposers = deque(proposers)
    proposer_level = defaultdict(int)
    next_round = []
    while proposers:
        proposer = proposers.popleft()
        i = proposer_level[proposer]
        if i < len(proposer.pref):
            partner = [partner for partner in partners 
                       if partner.name == proposer.pref[i]]
            if partner:
                match_found, removed_proposer = \
                    match(partner[0], proposer, result)
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

    return result, next_round

def match(partner, proposer, result):
    """Check and see if the proposer is the best match for the partner."""

    if partner not in result:
        result[partner] = proposer
        return True, None
    current_proposer = result[partner]
    proposer_rank = partner.get_rank(proposer)
    current_proposer_rank = partner.get_rank(current_proposer)
    if proposer_rank is not None and current_proposer_rank is not None:
        if proposer_rank < current_proposer_rank:
            result[partner] = proposer
            return True, current_proposer
    return False, None

def load_sisters_from_spreadsheet(filename, sister_type):
    """Convert excel spreadsheet to list of Sister objects."""

    book = xlrd.open_workbook(filename)
    first_sheet = book.sheet_by_index(0)
    col_names = first_sheet.row_values(0)
    rows = []
    for row_index in xrange(1, first_sheet.nrows):
        d = {'pref': []}
        for col_index in xrange(0, first_sheet.ncols):
            if col_names[col_index].startswith('pref'):
                d['pref'].append(first_sheet.cell(row_index, col_index).value)
            else:
                d[col_names[col_index]] = \
                    first_sheet.cell(row_index, col_index).value
        rows.append(d)
    
    result = []
    for row in rows:
        if sister_type == BIG_SISTER:
            result.append(BigSister(row['name'], row['pref'],
                          row['dying_family'], row['twins'], row['has_little'],
                          row['want']))
        elif sister_type == LITTLE_SISTER:
            result.append(LittleSister(row['name'], row['pref']))
        else:
            raise ValueError("sister type not supported")
    return result

def get_big_sisters(bigs, num_littles):
    """Decide who will be big sisters based on the number of littles."""

    # if there are not enough big sisters for all the little sisters, error out
    bigs_with_twins = [big for big in bigs if big.wants_twins]
    if num_littles > len(bigs_with_twins) + len(bigs):
        num_littles = num_littles - len(bigs_with_twins) - len(bigs)
        raise ValueError('Not enough bigs for all Littles, Need '
                         + str(num_littles) + ' more twins!')

    # big sisters who do not have a little sister and want one have the first priority
    first_priority_bigs = [big for big in bigs 
                           if not big.num_littles and big.want_level]
    if num_littles <= len(first_priority_bigs):
        return first_priority_bigs, None

    # big sisters who want a little but have a little sister are second priority
    second_priority_bigs = [big for big in bigs
                            if big.want_level and big.num_littles]
    if num_littles <= len(first_priority_bigs) + len(second_priority_bigs):
        second_priority_bigs.sort(reverse=True)
        return (first_priority_bigs + second_priority_bigs[:num_littles
                - len(first_priority_bigs)], None)

    # if there are not enough bigs, try adding twins
    bigs_with_twins = [big for big in bigs
                       if big.want_level and big.wants_twins]
    if num_littles <= len(first_priority_bigs) + \
                      len(second_priority_bigs) + len(bigs_with_twins):
        bigs_with_twins.sort(reverse=True)
        num_bigs_with_twins = \
            num_littles - len(first_priority_bigs) - len(second_priority_bigs)
        return (first_priority_bigs + second_priority_bigs,
                bigs_with_twins[:num_bigs_with_twins])

    # if there are not enough bigs with twins, and in last resort bigs
    third_priority_bigs = [big for big in bigs if not big.want_level]
    if num_littles <= len(bigs) + len(bigs_with_twins):
        number_last_bigs = len(bigs) + len(bigs_with_twins) - num_littles
        third_priority_bigs.sort(reverse=True)
        return (first_priority_bigs + second_priority_bigs
                + third_priority_bigs[:len(third_priority_bigs)
                - number_last_bigs], bigs_with_twins)
    return bigs, bigs_with_twins

def match_sisters(big_sisters, little_sisters):
    """Match bigs with littles so that the matching is stable."""

    big_sisters, bigs_with_twins = get_big_sisters(big_sisters,
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
    round1, little_sisters = matches(big_sisters, little_sisters)
    unmatched_big_sisters = [big_sister for big_sister in big_sisters
                             if big_sister not in round1.keys()]

    # for round 2, bigs have priority in choosing
    round2, big_sisters = matches(little_sisters,
                                  unmatched_big_sisters)
    unmatched_little_sisters = [little_sister 
                                for little_sister in little_sisters
                                if little_sister not in round2.keys()]

    # for round 3, arbitrarily match bigs and littles
    result = {}
    if unmatched_little_sisters:
        big_sisters.sort(reverse=True)
        priority_bigs = big_sisters[:len(unmatched_little_sisters)]
        for i in range(len(priority_bigs)):
            pbig = priority_bigs[i]
            result[pbig.name] = unmatched_little_sisters[i].name

    # combine all results
    for k, v in round1.iteritems():
        result[k.name] = v.name
    for k, v in round2.iteritems():
        result[v.name] = k.name
    return result

if __name__ == '__main__':
    filename1 = raw_input("Input Excel data for bigs: ")
    filename2 = raw_input("Input Excel data for littles: ")
    try:
        big_sisters = load_sisters_from_spreadsheet(filename1, BIG_SISTER)
        little_sisters = load_sisters_from_spreadsheet(filename2, LITTLE_SISTER)
        print match_sisters(big_sisters, little_sisters)
    except IOError:
        print "Check filenames!"
