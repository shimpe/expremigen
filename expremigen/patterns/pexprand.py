import math
import random
import sys

from expremigen.patterns.pattern import Pattern


class Pexprand(Pattern):
    def __init__(self, lo=1, hi=10, repeats=sys.maxsize):
        super().__init__()
        assert (lo * hi) > 0  # need same sign and != 0
        self.lo = lo
        self.hi = hi
        self.repeats = repeats

    def __str__(self):
        return "{0}({1}, {2}, {3})".format(self.__class__.__name__, self.lo, self.hi, self.repeats)

    def __iter__(self):
        for _ in range(self.repeats):
            yield self.lo * math.exp(math.log(self.hi / self.lo) * random.random())

    def __repr__(self):
        return self.__str__()
