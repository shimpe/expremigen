import itertools

from expremigen.patterns.pattern import Pattern
from expremigen.patterns.utils import take


class Pseries(Pattern):
    """
    pattern to generate an arithmetic series, e.g. Pseries(0, 1, 5) -> 0, 1, 2, 3, 4
    """

    def __init__(self, frm=0, step=1, length=5):
        super().__init__()
        self.frm = frm
        self.step = step
        self.length = length

    def __iter__(self):
        return take(self.length, itertools.count(self.frm, self.step))

    def __str__(self):
        return "{0}({1}, {2}, {3})".format(self.__class__.__name__, self.frm, self.step, self.length)
