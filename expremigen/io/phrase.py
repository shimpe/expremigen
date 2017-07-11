from expremigen.io.constants import PhraseProperty as PP, Defaults
from expremigen.musicalmappings.constants import REST
from expremigen.musicalmappings.note2midi import Note2Midi
from expremigen.patterns.pchord import Pchord
from expremigen.patterns.pconst import Pconst


class Phrase:
    """
    class to hold a Phrase, i.e. a collection of (animated) phrase properties
    """
    def __init__(self, properties: dict = None):
        self.n2m = Note2Midi()
        if properties is None:
            properties = {}
        self.p = properties
        if PP.NOTE not in self.p:
            self.p[PP.NOTE] = Pconst(self.n2m.lookup(Defaults.note), 1)
        if PP.DUR not in self.p:
            self.p[PP.DUR] = Pconst(Defaults.dur)
        if PP.LAG not in self.p:
            self.p[PP.LAG] = Pconst(Defaults.lag)
        if PP.PLAYEDDUR not in self.p:
            self.p[PP.PLAYEDDUR] = Pconst(Defaults.playeddur)
        if PP.VOL not in self.p:
            self.p[PP.VOL] = Pconst(Defaults.vol)
        if PP.TEMPO not in self.p:
            self.p[PP.TEMPO] = Pconst(Defaults.tempo)

        self.time = 0

    def __iter__(self):
        """
        converts the phrase to an iterable containing events
        :return: total time taken by this phrase
        """
        self.time = 0
        for value in zip(self.p[PP.NOTE], self.p[PP.DUR], self.p[PP.PLAYEDDUR], self.p[PP.VOL], self.p[PP.LAG],
                         self.p[PP.TEMPO]):
            if isinstance(value[0], Pchord) or value[0] != REST:  # 128 denotes a rest
                yield {PP.NOTE: value[0],
                       PP.DUR: value[1] * 4, # convert from quarter note to beat
                       PP.PLAYEDDUR: value[2],
                       PP.VOL: int(value[3]),
                       PP.LAG: value[4],
                       PP.TEMPO: value[5]
                       }
            self.time += value[1] * 4 # convert from quarter note to beat

    def generated_duration(self):
        # only works as expected after you iterated over the phrase
        return self.time
