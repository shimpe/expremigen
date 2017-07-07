import abc

from expremigen.pattern import Pattern


class Pbinop(Pattern, metaclass=abc.ABCMeta):
    def __init__(self, a: Pattern, b: Pattern) -> Pattern:
        super().__init__()
        self.a = a
        self.b = b

    def __str__(self):
        return "{0}({1}, {2})".format(self.__class__.__name__, self.a, self.b)