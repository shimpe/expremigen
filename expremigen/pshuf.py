import copy
import itertools
import math
import random

from expremigen.pattern import Pattern
from expremigen.pattern import flatten


def random_permutation(iterable, r=None):
    "Random selection from itertools.permutations(iterable, r)"
    pool = tuple(iterable)
    r = len(pool) if r is None else r
    return tuple(random.sample(pool, r))


def myrepeat(object, function, times=None):
    if times is None:
        while True:
            yield function(object)
    else:
        for i in range(times):
            yield function(object)


class Pshuf(Pattern):
    def __init__(self, alist=None, repeats=math.inf):
        super().__init__()
        if alist is None:
            alist = []
        self.alist = copy.deepcopy(alist)
        self.repeats = repeats

    def __iter__(self):
        # following shuffles the list after repeating
        # return (i for i in random_permutation(itertools.chain.from_iterable(itertools.repeat(self.alist, self.repeats))))

        # following shuffles the non-repeated list once and repeats it every time
        return (i for i in itertools.chain.from_iterable(itertools.repeat(random_permutation(self.alist), self.repeats)))

        # following reshuffles the non-repeated list over and over again
        #return flatten(i for i in itertools.chain.from_iterable(myrepeat(self.alist, random_permutation, self.repeats)))

    def __str__(self):
        return "{0}({1}, {2})".format(self.__class__.__name__, self.alist, self.repeats)
