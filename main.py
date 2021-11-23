import unittest

import hypothesis.strategies as st
from hypothesis import note, settings, assume
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant

TOTAL_DISCS = 3
MAX_EXAMPLES = 2000

# select one of the 3 pegs
peg_strategy = st.integers(min_value=0, max_value=2)


class TowerOfHanoi(RuleBasedStateMachine):

    def __init__(self):
        super().__init__()
        self.completed_tower = [x for x in reversed(range(1, TOTAL_DISCS + 1))]
        self.peg_data = [
            self.completed_tower.copy(),
            [],
            [],
        ]

    @rule(from_peg=peg_strategy, to_peg=peg_strategy)
    def move(self, from_peg, to_peg):
        try:
            disc = self.peg_data[from_peg].pop()
        except IndexError:
            # Trying to move from a peg with no discs
            # Using an assume() here would discard too many tests
            pass
        else:
            self.peg_data[to_peg].append(disc)

    @staticmethod
    def is_sorted(l):
        return all(l[i] >= l[i + 1] for i in range(len(l) - 1))

    @invariant()
    def only_smaller_on_bigger(self):
        for peg in self.peg_data:
            # check if peg has any discs
            if peg:
                # reject if larger discs are on top of smaller discs
                assume(self.is_sorted(peg))

    @invariant()
    def problem_not_solved(self):
        note(f"> {self.peg_data}")
        assert self.peg_data != [[], [], self.completed_tower]


TowerOfHanoi.TestCase.settings = settings(max_examples=MAX_EXAMPLES)

TowerOfHanoiTest = TowerOfHanoi.TestCase

if __name__ == '__main__':
    unittest.main()
