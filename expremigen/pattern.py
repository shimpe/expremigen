import abc


class Pattern(metaclass=abc.ABCMeta):
    def __str__(self):
        return "{0}".format(self.__class__.__name__)


def flatten(l):
    for el in l:
        if isinstance(el, Pattern):
            yield from flatten(el)
        else:
            yield el
