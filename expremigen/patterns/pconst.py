import itertools
import sys

from expremigen.patterns.pattern import Pattern
from expremigen.patterns.utils import flatten


class Pconst(Pattern):
    """
    pattern that returns a given "constant" for "repeats" time
    """

    def __init__(self, constant=0, repeats=sys.maxsize):
        super().__init__()
        self.constant = constant
        self.repeats = repeats

    def __str__(self):
        return "{0}({1}, {2})".format(self.__class__.__name__, self.constant, self.repeats)

    def __iter__(self):
        return flatten(c for c in itertools.repeat(self.constant, self.repeats))

    def __repr__(self):
        return self.__str__()
