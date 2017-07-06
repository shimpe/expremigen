import abc


class Pattern(metaclass=abc.ABCMeta):
    def __str__(self):
        return "{0}".format(self.__class__.__name__)
