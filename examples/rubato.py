from vectortween.NumberAnimation import NumberAnimation
from vectortween.SequentialAnimation import SequentialAnimation

from expremigen.io.constants import PhraseProperty as PP
from expremigen.io.pat2midi import Pat2Midi
from expremigen.io.phrase import Phrase
from expremigen.musicalmappings.durations import Durations as Dur
from expremigen.musicalmappings.dynamics import Dynamics as Dyn
from expremigen.musicalmappings.note2midi import Note2Midi
from expremigen.patterns.pconst import Pconst
from expremigen.patterns.pseq import Pseq
from expremigen.patterns.ptween import Ptween

outputfile = "output/rubato.mid"


def create_phrase():
    p = Pat2Midi()
    n = Note2Midi()

    # vary the lag to create the rubato feeling
    lag_inc = NumberAnimation(frm=0, to=0.3, tween=['easeOutQuad'])
    lag_dec = NumberAnimation(frm=0.3, to=0, tween=['easeInOutCubic'])
    lag = SequentialAnimation([lag_inc, lag_dec], [1, 3], 2)

    # vary the volume over time to keep it interesting
    vol_inc1 = NumberAnimation(frm=Dyn.f, to=Dyn.ff, tween=['linear'])
    vol_dec1 = NumberAnimation(frm=Dyn.ff, to=Dyn.mf, tween=['linear'])

    vol_inc2 = NumberAnimation(frm=Dyn.mf, to=Dyn.f, tween=['linear'])
    vol_dec2 = NumberAnimation(frm=Dyn.f, to=Dyn.mp, tween=['linear'])

    vol_inc3 = NumberAnimation(frm=Dyn.mp, to=Dyn.mf, tween=['linear'])
    vol_dec3 = NumberAnimation(frm=Dyn.mf, to=Dyn.pp, tween=['linear'])
    vol = SequentialAnimation([vol_inc1, vol_dec1, vol_inc2, vol_dec2, vol_inc3, vol_dec3])

    # and why not bounce a bit between legato and staccato while we're having fun?
    legato_to_staccato = NumberAnimation(frm=1, to=0.25, tween=['easeOutBounce'])
    staccato_to_legato = NumberAnimation(frm=0.1, to=1, tween=['easeOutBounce'])
    dur = SequentialAnimation([legato_to_staccato, staccato_to_legato])

    # animate the tempo
    tempo_slowdown = NumberAnimation(frm=120, to=80, tween=['easeOutQuad'])

    # play some random cadenza
    notes = n.convert2(
        "a5 b5 c6 a5 e5 d5 c5 d5 e5 c5 a4 g#4 a4 b4 c5 a4 e4 d4 c4 d4 e4 c4 a3 g#3 a3 b3 c4 d4 e4 g#4 a4".split(" "))
    notes2 = n.convert2(
        "d4 e4 f4 d4 a3 g3 f3 g3 a3 b3 c4 d4 c4 d4 e4 c4 g3 f3 e3 f3 g3 a3 b3 c4 a3 b3 c4 d4 e4 g#4 a4".split(" "))
    notes.extend(notes2)

    properties_plain = {
        PP.NOTE: Pseq(notes, 1),
        PP.VOL: Pconst(100),
        PP.PLAYEDDUR: Pconst(0.95),
        PP.DUR: Pseq([Pconst(Dur.sixteenth_triplet, len(notes2) - 1), Pconst(Dur.half, 1)], 2),
        PP.LAG: Pconst(0),
        PP.TEMPO: Pconst(120)
    }
    properties_rubato = {
        PP.NOTE: Pseq(notes, 1),
        PP.VOL: Ptween(vol, 0, 0, len(notes), len(notes), None),
        PP.PLAYEDDUR: Ptween(dur, 0, 0, len(notes), len(notes), None),
        PP.DUR: Pseq([Pconst(Dur.sixteenth_triplet, len(notes2) - 1), Pconst(Dur.half, 1)], 2),
        PP.LAG: Ptween(lag, 0, 0, len(notes), len(notes), None),
        PP.TEMPO: Ptween(tempo_slowdown, 0, 0, len(notes), len(notes), None)
    }

    ph = Phrase(properties_plain)
    ph2 = Phrase(properties_rubato)
    p.add_phrases([ph, ph2], 0, 0, 0)

    p.write(outputfile)


if __name__ == "__main__":
    create_phrase()
