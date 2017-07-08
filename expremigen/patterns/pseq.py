import copy
import itertools
import math

from expremigen.patterns.utils import flatten
from expremigen.patterns.pattern import Pattern


class Pseq(Pattern):
    def __init__(self, alist=None, repeats=math.inf):
        super().__init__()
        if alist is None:
            alist = []
        self.alist = copy.deepcopy(alist)
        self.repeats = repeats

    def __iter__(self):
        return flatten(j for i in itertools.repeat(self.alist, self.repeats) for j in i)

    def __str__(self):
        return "{0}({1}, {2})".format(self.__class__.__name__, self.alist, self.repeats)
