import random
from expremigen.pattern import Pattern

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

def flatten(l):
    for el in l:
        if isinstance(el, Pattern):
            yield from flatten(el)
        else:
            yield el

import itertools
def take(n, iterable):
    "Return first n items of the iterable as a list"
    return itertools.islice(iterable, n)
