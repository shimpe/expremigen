from vectortween.Animation import Animation

from expremigen.patterns.pattern import Pattern


class Ptween(Pattern):
    """
    class to glue pyvectortween to expremigen
    """

    def __init__(self, animation: Animation, birthframe=0, startframe=0, stopframe=0,
                 deathframe=0, noiseframe=None):
        super().__init__()
        self.animation = animation
        self.bf = birthframe
        self.staf = startframe
        self.stof = stopframe
        self.df = deathframe
        self.nf = noiseframe
        self.current_frame = 0

    def __iter__(self):
        for i in range(int(self.df)):
            yield self.animation.make_frame(i, self.bf, self.staf, self.stof, self.df, self.nf)

    def __str__(self):
        return "{0}(<anim>, {1}, {2}, {3}, {4}, {5})".format(self.__class__.__name__, self.bf,
                                                             self.staf, self.stof, self.df, self.nf)
