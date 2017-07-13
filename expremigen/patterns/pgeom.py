from expremigen.patterns.pattern import Pattern
from expremigen.patterns.utils import take, geom


class Pgeom(Pattern):
    """
    pattern that generates numbers in geometric series, e.g. Pgeom(1, 2, 5) -> 1, 2, 4, 8, 16
    """

    def __init__(self, frm=0, factor=1, length=5):
        """

        :param frm: starting number
        :param factor: factor by which to keep multiplying the starting number
        :param length: length of generated sequence
        """
        super().__init__()
        self.frm = frm
        self.factor = factor
        self.length = length

    def __iter__(self):
        return take(self.length, geom(self.frm, self.factor))

    def __str__(self):
        return "{0}({1}, {2}, {3})".format(self.__class__.__name__, self.frm, self.factor, self.length)
