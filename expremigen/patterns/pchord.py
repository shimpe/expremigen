from expremigen.patterns.pattern import Pattern


class Pchord(Pattern):
    """
    special pattern that is never flattened; interpreted as a chord by the rest of the system
    """

    def __init__(self, notes=0):
        super().__init__()
        self.notes = notes

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.notes)

    def __iter__(self):
        yield Pchord(self.notes)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.notes == other.notes
