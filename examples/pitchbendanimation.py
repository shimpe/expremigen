from vectortween.NumberAnimation import NumberAnimation
from vectortween.SequentialAnimation import SequentialAnimation

from expremigen.io.constants import PhraseProperty as PP
from expremigen.io.midicontrolchanges import MidiControlChanges as MCC
from expremigen.io.pat2midi import Pat2Midi
from expremigen.io.phrase import Phrase
from expremigen.musicalmappings.durations import Durations as Dur
from expremigen.musicalmappings.note2midi import Note2Midi
from expremigen.patterns.pconst import Pconst
from expremigen.patterns.ptween import Ptween

outputfile = "output/pitchbendanimation.mid"


def create_phrase():
    n = Note2Midi()
    a = NumberAnimation(frm=0, to=8000, tween=['easeOutElastic', 1, 0.02])
    b = NumberAnimation(frm=8000, to=0, tween=['easeOutElastic', 1, 0.02])
    c = NumberAnimation(frm=0, to=-8000, tween=['easeOutBounce', 0.1, 0.02])
    d = NumberAnimation(frm=-8000, to=0, tween=['easeOutBounce', 0.1, 0.02])
    s = SequentialAnimation([a, b, c, d], repeats=10)
    properties = {
        PP.NOTE: n.convert2(Pconst("a4", 1)),
        PP.DUR: Pconst(Dur.whole * 16, 1),  # single note for 16 beats
        PP.PLAYEDDUR: Pconst(1),
        PP.ctrl_dur_key(MCC.PitchWheel): Pconst(0.03125,
                                              int((1 / 0.03125) * Dur.whole * 16)),
        PP.ctrl_val_key(MCC.PitchWheel): Ptween(s,
                                              0,
                                              0,
                                              int((1 / 0.03125) * Dur.whole * 16) - 1,
                                              int((1 / 0.03125) * Dur.whole * 16) - 1,
                                              None)
    }
    p = Phrase(properties)
    p2m = Pat2Midi()
    p2m.add_phrase(p, track=0, channel=0, start_time=0)
    p2m.write(outputfile)


if __name__ == "__main__":
    create_phrase()
