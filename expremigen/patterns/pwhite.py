import random
import sys

from expremigen.patterns.pattern import Pattern


class Pwhite(Pattern):
    """
    class to generate random numbers
    """

    def __init__(self, lo=0, hi=1, repeats=sys.maxsize):
        super().__init__()
        self.lo = lo
        self.hi = hi
        self.repeats = repeats

    def __str__(self):
        return "{0}({1}, {2}, {3})".format(self.__class__.__name__, self.lo, self.hi, self.repeats)

    def __iter__(self):
        for _ in range(self.repeats):
            yield random.uniform(self.lo, self.hi)

    def __repr__(self):
        return self.__str__()
