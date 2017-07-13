import copy
import itertools
import sys

from expremigen.patterns.pattern import Pattern
from expremigen.patterns.utils import random_permutation


class Pshuf(Pattern):
    """
    pattern to randomly shuffle elements from a list; the randomly shuffled list
    then is repeated verbatim for repats times
    """

    def __init__(self, alist=None, repeats=sys.maxsize):
        super().__init__()
        if alist is None:
            alist = []
        self.alist = copy.deepcopy(alist)
        self.repeats = repeats

    def __iter__(self):
        # following shuffles the list after repeating
        # return (i for i in random_permutation(itertools.chain.from_iterable(itertools.repeat(self.alist,
        # self.repeats))))

        # following shuffles the non-repeated list once and repeats it every time
        return (i for i in
                itertools.chain.from_iterable(itertools.repeat(random_permutation(self.alist), self.repeats)))

        # following reshuffles the non-repeated list over and over again
        # return flatten(i for i in itertools.chain.from_iterable(myrepeat(self.alist, random_permutation,
        # self.repeats)))

    def __str__(self):
        return "{0}({1}, {2})".format(self.__class__.__name__, self.alist, self.repeats)
