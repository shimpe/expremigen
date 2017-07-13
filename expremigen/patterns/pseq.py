import copy
import itertools
import sys

from expremigen.patterns.pattern import Pattern
from expremigen.patterns.utils import flatten


class Pseq(Pattern):
    """
    pattern that generates numbers one by one from a list
    """

    def __init__(self, alist=None, repeats=sys.maxsize):
        super().__init__()
        if alist is None:
            alist = []
        self.alist = copy.deepcopy(alist)
        self.repeats = repeats

    def __iter__(self):
        return flatten(j for i in itertools.repeat(self.alist, self.repeats) for j in i)

    def __str__(self):
        return "{0}({1}, {2})".format(self.__class__.__name__, self.alist, self.repeats)
