from random import random
from matplotlib import pyplot as plt
import numpy as np

# Constants
BASE_RATIOS = {'A': 0.1, 'G': 0.4, 'C': 0.2, 'T': 0.3}
EOL = '$'

def rand_sequence(length):
    """Generates a random DNA sequence according to the base ratios."""
    sequence = []
    for _ in xrange(length):
        uniform = random()
        prob_helper = 0
        for base, ratio in BASE_RATIOS.iteritems():
            prob_helper += ratio
            if uniform <= prob_helper:
                sequence.append(base)
                break
    sequence.append(EOL)
    return ''.join(sequence)

class Node(object):
    """Class representing a node in the prefix tree"""

    def __init__(self, name):
        self.name = name
        self.transitions = {}

    def set_name(self, new_name):
        self.name = new_name

    def set_transition(self, key, node):
        self.transitions[key] = node

    def get_child(self, key):
        return self.transitions[key]

    def get_name(self):
        return self.name

    def __str__(self):
        to_return = []
        to_return.append('Name: %s' % self.name)
        for key, value in self.transitions.iteritems():
            to_return.append('%s: %s' % (key, value.name))
        to_return.append('\n')
        return '\n'.join(to_return)


def form_suffix_tree(sequence, get_root=False):
    """Forms a prefix tree and returns length of longest repeated substring."""
    root = Node('')
    longest_substring = 0
    for index in xrange(len(sequence) - 2, -1, -1):
        substring_length = _add_state_to_tree(root, sequence[index:])
        if substring_length > longest_substring:
            longest_substring = substring_length
    if get_root:
        return (longest_substring, root)
    return longest_substring

def _add_state_to_tree(root, subseq):
    """Helper function for adding state. Returns longest matching substring."""
    score = len(root.get_name())
    if subseq[0] not in root.transitions.keys():
        child = Node(subseq)
        root.set_transition(subseq[0], child)
        return score
    else:
        child = root.get_child(subseq[0])
        child_name = child.get_name()
        # Find longest common prefix.
        match_index = -1
        for index in xrange(min(len(child_name), len(subseq))):
            if child_name[index] != subseq[index]:
                break
            else:
                match_index = index
        # If full match with child name...
        if match_index == len(child_name) - 1:
            if match_index < len(subseq) - 1:
                return score +  _add_state_to_tree(child, subseq[match_index + 1:])
            # Otherwise do nothing because already happened, don't this case
            # ever happens though.
        else:
            # Create new parent to insert inbetween
            parent = Node(child_name[:match_index + 1])
            root.set_transition(subseq[0], parent)
            # Reconfigure child's name and make child of parent.
            child.set_name(child_name[match_index + 1:])
            parent.set_transition(child_name[match_index + 1], child)
            # Create a new child for the newly added parent.
            new_child = Node(subseq[match_index + 1:])
            parent.set_transition(subseq[match_index + 1], new_child)
            return score + len(parent.get_name())

def sim_data(length, trials):
    """Simulates the value of K given length of string and trials."""
    data = []
    for _ in xrange(trials):
        string = rand_sequence(length)
        data.append(form_suffix_tree(string) + 1)
    return data

def make_hist(data, length):
    plt.hist(data, bins=np.arange(min(data) - 0.5, max(data) + 0.5, 1), alpha=0.75)
    plt.xlabel('K')
    plt.ylabel('Frequency')
    plt.title('K Histogram for Length = ' + str(length))
    lower_bound = np.log(length + 1) / np.log(1 / 0.4)
    plt.axvline(lower_bound, color='r', linestyle='dashed', linewidth=2)
    plt.show()

def run_sims(lengths, trials):
    """Run the desired sims and output hists given list of lengths."""
    for length in lengths:
        data = sim_data(length, trials)
        make_hist(data, length)

def sanity_test():
    print(form_suffix_tree('mississippi$'))
    print(form_suffix_tree('bananas$'))
    print(form_suffix_tree('GTCCGAAGCTCCGG$'))
    print(form_suffix_tree('ATGCACA$'))

    for _ in range(5):
        string = rand_sequence(32)
        print string, form_suffix_tree(string)

def print_tree(root):
    print root
    for child in root.transitions.values():
        print_tree(child)

if __name__ == '__main__':
    # sanity_test()
    run_sims([2 ** i for i in range(5, 10)], 10000)
