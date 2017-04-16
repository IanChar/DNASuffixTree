
from __future__ import division
import SubstringAnalysis as SA

FILENAME = 'DNA.txt'

def get_dna():
    sequence = []
    with open(FILENAME) as f:
        for line in f:
            sequence.append(line[:-1])
    return ''.join(sequence)

def get_proportions():
    counts = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
    sequence = get_dna()
    for base in sequence:
        if base not in counts.keys():
            raise TypeError('Non-base character %d' % ord(base))
        counts[base] += 1
    return {base: count / len(sequence) for base, count in counts.iteritems()}

def get_kval():
    sequence = get_dna()
    sequence += '$'
    return SA.form_suffix_tree(sequence)

if __name__ == '__main__':
    print len(get_dna())
