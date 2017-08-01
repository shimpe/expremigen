from expremigen.io.constants import PhraseProperty as PP, Defaults, NO_OF_CONTROLLERS, NO_OF_OFFICIAL_CONTROLLERS
from expremigen.io.midicontrolchanges import MidiControlChanges as MCC
from expremigen.musicalmappings.constants import REST
from expremigen.musicalmappings.note2midi import Note2Midi
from expremigen.patterns.pchord import Pchord
from expremigen.patterns.pconst import Pconst


class Phrase:
    """
    class to hold a Phrase, i.e. a dictionary of (animated) phrase properties
    The key is one of
        PhraseProperty.NOTE,
        PhraseProperty.DUR,
        PhraseProperty.LAG,
        PhraseProperty.PLAYEDDUR,
        PhraseProperty.VOL,
        PhraseProperty.TEMPO,
        PhraseProperty.CtrlDur(CCNumber)
        PhraseProperty.CtrlVal(CCNumber)
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

        self.note_time = 0
        self.ctrl_time = [0 for _ in range(NO_OF_CONTROLLERS)]

    def __iter__(self):
        """
        converts the phrase to an iterable containing events

        :return: total time taken by this phrase
        """
        self.note_time = 0
        self.ctrl_time = [0 for _ in range(NO_OF_CONTROLLERS)]

        # note events are basically governed by the DUR key
        for value in zip(self.p[PP.NOTE], self.p[PP.DUR], self.p[PP.PLAYEDDUR], self.p[PP.VOL], self.p[PP.LAG],
                         self.p[PP.TEMPO]):
            if isinstance(value[0], Pchord) or value[0] != REST:  # 128 denotes a rest
                yield {
                    PP.NOTE: value[0],
                    PP.DUR: value[1] * 4,  # convert from quarter note to beat
                    PP.PLAYEDDUR: value[2],
                    PP.VOL: int(value[3]),
                    PP.LAG: value[4],
                    PP.TEMPO: value[5]
                }
            self.note_time += value[1] * 4  # convert from quarter note to beat

        # control change events can have their own timeline (e.g. this allows for pitchbend or modwheel variations
        # while notes are playing)
        for cc in range(NO_OF_OFFICIAL_CONTROLLERS):
            if PP.ctrl_dur_key(cc) in self.p and PP.ctrl_val_key(cc) in self.p:
                for value in zip(self.p[PP.ctrl_dur_key(cc)], self.p[PP.ctrl_val_key(cc)]):
                    if value[0] is not None and value[1] is not None:
                        yield {
                            PP.ctrl_dur_key(cc): value[0] * 4,
                            PP.ctrl_val_key(cc): value[1]
                        }
                    self.ctrl_time[cc] += value[0] * 4
        for cc in [MCC.PitchWheel]:
            if PP.ctrl_dur_key(cc) in self.p and PP.ctrl_val_key(cc) in self.p:
                for value in zip(self.p[PP.ctrl_dur_key(cc)], self.p[PP.ctrl_val_key(cc)]):
                    if value[0] is not None and value[1] is not None:
                        yield {
                            PP.ctrl_dur_key(cc): value[0] * 4,
                            PP.ctrl_val_key(cc): int(value[1])
                        }
                    self.ctrl_time[cc] += value[0] * 4

    def generated_duration(self):
        """

        :return: total duration of this note phrase
        """
        # only works as expected after you iterated over the phrase already
        return self.note_time

    def generated_ctrl_duration(self, cc_value):
        """
        :param cc_value: midi control change id
        :return: total duration taken by control changes for controller cc_value
        """
        # only works as expected after you iterated over the phrase already
        return self.ctrl_time[cc_value]
