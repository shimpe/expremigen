import random

from expremigen.patterns.pattern import Pattern
from expremigen.patterns.pchord import Pchord


def random_permutation(iterable, r=None):
    "Random selection from itertools.permutations(iterable, r)"
    pool = tuple(iterable)
    r = len(pool) if r is None else r
    return tuple(random.sample(pool, r))


def myrepeat(object, function, times=None):
    if times is None:
        while True:
            if function is not None:
                yield function(object)
            else:
                yield object
    else:
        for i in range(times):
            if function is not None:
                yield function(object)
            else:
                yield object


def flatten(l):
    for el in l:
        if isinstance(el, Pattern) and not isinstance(el, Pchord):
            yield from flatten(el)
        else:
            yield el


import itertools


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return itertools.islice(iterable, n)


def geom(start=1, factor=2):
    # geom(1) --> 1 2 4 8 ...
    # geom(16, 0.5) -> 16 8 4 2 1 0.5 ...
    n = start
    while True:
        yield n
        n *= factor
