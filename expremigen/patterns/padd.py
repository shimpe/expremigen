import itertools
import operator

from expremigen.patterns.pattern import Pattern
from expremigen.patterns.pbinop import Pbinop
from expremigen.patterns.utils import flatten


class Padd(Pbinop):
    """
    pattern that returns the sum of two other patterns
    """

    def __init__(self, a: Pattern, b: Pattern):
        super().__init__(a, b)

    def __iter__(self):
        return flatten(i for i in itertools.starmap(operator.__add__, zip(self.a, self.b)))
