import abc


class Pattern(metaclass=abc.ABCMeta):
    """
    abstract base class for a Pattern
    """

    def __str__(self):
        return "{0}".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()
