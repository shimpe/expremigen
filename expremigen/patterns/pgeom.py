from expremigen.patterns.utils import take, geom
from expremigen.patterns.pattern import Pattern


class Pgeom(Pattern):
    def __init__(self, frm=0, factor=1, length=5):
        super().__init__()
        self.frm = frm
        self.factor = factor
        self.length = length

    def __iter__(self):
        return take(self.length, geom(self.frm, self.factor))

    def __str__(self):
        return "{0}({1}, {2}, {3})".format(self.__class__.__name__, self.frm, self.factor, self.length)
