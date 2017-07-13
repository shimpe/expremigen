import copy
import itertools
import sys

from expremigen.patterns.pattern import Pattern
from expremigen.patterns.utils import flatten, take
from expremigen.patterns.utils import random_permutation


class Prand(Pattern):
    """
    Pattern used to draw random numbers from a list
    (numbers may repeat themselves)
    """

    def __init__(self, alist=None, repeats=sys.maxsize):
        """
        pattern that
        :param alist: possible numbers
        :param repeats: how many numbers to draw
        """
        super().__init__()
        if alist is None:
            alist = []
        self.alist = copy.deepcopy(alist)
        self.repeats = repeats

    def __iter__(self):
        # following shuffles the list after repeating
        return flatten(take(self.repeats, (i for i in random_permutation(
            itertools.chain.from_iterable(itertools.repeat(self.alist, self.repeats))))))

    def __str__(self):
        return "{0}({1}, {2})".format(self.__class__.__name__, self.alist, self.repeats)
