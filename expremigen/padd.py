import itertools
import operator

from expremigen.pattern import Pattern
from expremigen.pbinop import Pbinop


class Padd(Pbinop):
    def __init__(self, a: Pattern, b: Pattern):
        super().__init__(a, b)

    def __iter__(self):
        return (i for i in itertools.starmap(operator.__add__, zip(self.a, self.b)))
