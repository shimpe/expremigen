from expremigen.io.constants import PhraseProperty as PP
from expremigen.io.pat2midi import Pat2Midi
from expremigen.io.phrase import Phrase
from expremigen.musicalmappings.durations import Durations as Dur
from expremigen.musicalmappings.dynamics import Dynamics as Dyn
from expremigen.musicalmappings.note2midi import Note2Midi
from expremigen.patterns.pchord import Pchord as C
from expremigen.patterns.pconst import Pconst
from expremigen.patterns.pseq import Pseq
from expremigen.patterns.ptween import Ptween

outputfile = "output/twovoicewithchords.mid"


def add_melody(pat2mid, track, channel):
    n = Note2Midi()
    notes = ["c4", "e4", "g4", "c5", "b4", "g4", "f4", "d4", "c4"]
    from vectortween.NumberAnimation import NumberAnimation
    from vectortween.SequentialAnimation import SequentialAnimation
    increase = NumberAnimation(frm=Dyn.mp, to=Dyn.f)
    decrease = NumberAnimation(frm=Dyn.f, to=Dyn.ppp)
    swell_dim = SequentialAnimation([increase, decrease])
    increasing_staccato = NumberAnimation(frm=1, to=0.5)
    properties = {
        # convert from note names to midi numbers
        PP.NOTE: Pseq(n.convert2(notes)),
        # last note is longer than the rest
        PP.DUR: Pseq([Pconst(Dur.quarter, len(notes) - 1), Pconst(Dur.whole, 1)]),
        # animate staccato
        PP.PLAYEDDUR: Ptween(increasing_staccato, 0, 0, len(notes), len(notes)),
        # volume should linearly go up from mp to f, then go down from f to ppp as the phrase progresses
        PP.VOL: Ptween(swell_dim, 0, 0, len(notes), len(notes), None),
    }
    p = Phrase(properties)
    pat2mid.set_tempo(60)
    pat2mid.add_phrase(p, track=track, channel=channel, start_time=0)
    return pat2mid


def add_chords(pat2mid, track, channel):
    n = Note2Midi()
    notes = [C(["c3", "e3", "g3"]), C(["b2", "d3", "g3"]), C(["c3", "e3", "g3", "c4"])]
    from vectortween.NumberAnimation import NumberAnimation
    decrease = NumberAnimation(frm=Dyn.f, to=Dyn.p)
    properties = {
        PP.NOTE: Pseq(n.convert2(notes)),
        PP.DUR: Pseq([Pconst(Dur.whole, 2), Pconst(Dur.doublewhole, 1)]),
        PP.PLAYEDDUR: Pconst(1),
        PP.VOL: Ptween(decrease, 0, 0, len(notes), len(notes), None)
    }
    p = Phrase(properties)
    pat2mid.add_phrase(p, track=track, channel=channel, start_time=0)
    return pat2mid


if __name__ == "__main__":
    p2m = Pat2Midi(num_tracks=2)
    p2m = add_melody(p2m, 0, 0)
    p2m = add_chords(p2m, 1, 1)
    p2m.write(outputfile)
