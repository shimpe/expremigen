import itertools
import random

from expremigen.patterns.pattern import Pattern
from expremigen.patterns.pchord import Pchord


def random_permutation(iterable, r=None):
    """Random selection from itertools.permutations(iterable, r)"""
    pool = tuple(iterable)
    r = len(pool) if r is None else r
    return tuple(random.sample(pool, r))


def myrepeat(what, fn, times=None):
    """

    :param what: something to repeat
    :param fn: extra function to apply
    :param times: number of times to repeat
    :return:
    """
    if times is None:
        while True:
            if fn is not None:
                yield fn(what)
            else:
                yield what
    else:
        for i in range(times):
            if fn is not None:
                yield fn(what)
            else:
                yield what


def flatten(l):
    """

    :param l: list l
    :return: iterator to flatten list l; Pchord are not flattened
    """
    for el in l:
        if isinstance(el, Pattern) and not isinstance(el, Pchord):
            yield from flatten(el)
        else:
            yield el


def take(n, iterable):
    """Return first n items of the iterable as a list"""
    return itertools.islice(iterable, n)


def geom(start=1, factor=2):
    """
    iterator to generate geometric series
    :param start: start number
    :param factor: constant factor to apply
    :return: geometric series, e.g. geom(16, 0.5) -> 16 8 4 2 1 0.5 ...
    """
    # geom(1) --> 1 2 4 8 ...
    # geom(16, 0.5) -> 16 8 4 2 1 0.5 ...
    n = start
    while True:
        yield n
        n *= factor
