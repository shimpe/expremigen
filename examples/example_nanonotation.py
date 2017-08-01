from itertools import tee

from vectortween.NumberAnimation import NumberAnimation
from vectortween.SequentialAnimation import SequentialAnimation

from expremigen.io.constants import PhraseProperty as PP
from expremigen.io.pat2midi import Pat2Midi
from expremigen.io.phrase import Phrase
from expremigen.musicalmappings.dynamics import Dynamics as Dyn
from expremigen.musicalmappings.nanonotation import NanoNotation
from expremigen.musicalmappings.note2midi import Note2Midi
from expremigen.musicalmappings.playeddurations import PlayedDurations as PDur
from expremigen.patterns.pconst import Pconst
from expremigen.patterns.pseq import Pseq
from expremigen.patterns.ptween import Ptween

outputfile = "output/example_nanonotation.mid"


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class PhraseFactory:
    def __init__(self):
        self.note2midi = Note2Midi()
        self.nano = NanoNotation()

    def __call__(self,
                 kind=None,
                 nanonotation=None,
                 volumes=None,
                 last_note_is_final=False):
        notes = self.nano.notes(nanonotation)
        durations = self.nano.dur(nanonotation)
        return Phrase({
            PP.NOTE: self.note(notes),
            PP.VOL: self.volume(notes, volumes, None, None),
            PP.PLAYEDDUR: self.playeddur(notes, kind),
            PP.DUR: self.dur(durations),
            PP.LAG: self.lag(notes, last_note_is_final)
        })

    @classmethod
    def playeddur(cls, notes, kind="l2s"):
        """
        :param notes: list of notes that make up the phrase
        :param kind: one of "l2s" (legato-to-staccato) or "s2l" (staccato-to-legato)
        :return: pattern that generates the desired playeddur values
        """
        if kind == "l2s":
            anim = Pseq([Pconst(PDur.legato, len(notes) - 1), Pconst(PDur.staccato, 1)], 1)
        elif kind == "s2l":
            anim = Pseq([Pconst(PDur.staccato, len(notes) - 1), Pconst(PDur.legato, 1)], 1)
        elif kind == "s2s":
            anim = Pconst(PDur.staccato, len(notes))
        elif kind == "l2l":
            anim = Pconst(PDur.legato, len(notes))
        else:
            anim = None
            assert False
        return anim

    @classmethod
    def volume(cls, notes, volumes=None, individual_tween=None, overall_tween=None):
        """
        :param notes: list of notes that make up the phrase
        :param volumes: a list of volumes to evolve to over the course of the phrase, e.g. [Dyn.mp, Dyn.mf, Dyn.ppp]
        :param individual_tween: per segment tween
        :param overall_tween: tween over all segments
        :return: pattern that tweens between the successive volumes
        """
        if volumes is None:
            volumes = [Dyn.mf, Dyn.mf]
        if overall_tween is None:
            overall_tween = ['linear']
        if individual_tween is None:
            individual_tween = ['linear']
        if len(volumes) == 1:
            volumes = [volumes[0], volumes[0]]
        anims = []
        for v in pairwise(volumes):
            anims.append(NumberAnimation(frm=v[0], to=v[1], tween=individual_tween))
        s = SequentialAnimation(anims, tween=overall_tween)
        return Ptween(s, 0, 0, len(notes), len(notes))

    def note(self, notes):
        """
        :param notes: list of notes that make up the phrase
        :return: pattern that generates the notes one by one
        """
        return Pseq(self.note2midi.convert2(notes))

    @classmethod
    def lag(cls, notes, last_note_is_endnote=False):
        """
        :param last_note_is_endnote:
        :param notes: list of notes that make up the phrase
        :return: pattern that generates the desired lag
        """
        if last_note_is_endnote:
            return Pseq([Pconst(0, len(notes) - 1), Pconst(0.5, 1)], repeats=1)
        else:
            return Pconst(0, len(notes))

    @classmethod
    def dur(cls, durations):
        return Pseq(durations, repeats=1)


def play_bach():
    p2m = Pat2Midi(num_tracks=2)
    ff = PhraseFactory()

    # upper voice
    uppervoice = []
    uppervoice_fragments = [
        ["l2s", "r_16 e4 a c5 b4 e b d5 c_8", [Dyn.f, Dyn.ff]],
        ["s2s", "e5_8 g#4 e5 a4_16", [Dyn.ff, Dyn.f]],
        ["l2s", "e4_16 a4 c5 b4 e b d5 c_8", [Dyn.f, Dyn.ff]],
        ["s2s", "a4_8 r_4", [Dyn.f]],
        ["l2s", "r_16 e5 c e a4 c5 e4 g f_8", [Dyn.p, Dyn.ff]],
        ["s2l", "a4_8 d5 f_8.", [Dyn.f, Dyn.p]],
        ["s2l", "d5_16 b4 d5 g4 b d f e_8", [Dyn.p, Dyn.ff]],
        ["s2l", "g4 c5 e_8.", [Dyn.f, Dyn.p]],
        ["l2s", "c5_16 a4 c5 f4_8", [Dyn.p, Dyn.ff]],
        ["s2l", "d5_8. b4_16 g b e_8", [Dyn.p, Dyn.ff]],
        ["l2s", "c5_8. a4_16 f a d_8", [Dyn.p, Dyn.ff]],
        ["s2s", "b4_8 c5_8 r_8 r_4", [Dyn.ff]]
    ]
    for fragment in uppervoice_fragments:
        uppervoice.append(ff(type=fragment[0],
                             nanonotation=fragment[1],
                             volumes=fragment[2]))

    lowervoice = []
    lowervoice_fragments = [
        ["s2s", "a2_8", [Dyn.mf]],
        ["l2s", "a3_4 g#_8 a_16", [Dyn.f, Dyn.mf, Dyn.f]],
        ["l2s", "e3_16 a c4 b3 e b d4 c_8", [Dyn.f, Dyn.ff]],
        ["s2s", "a3_8 g# e a_16", [Dyn.ff, Dyn.f]],
        ["l2s", "e3_16 a c4 b3 e b d4 c_8", [Dyn.f, Dyn.ff]],
        ["s2s", "a3_8 c4 a3 d4_16", [Dyn.ff, Dyn.f]],
        ["l2s", "a3_16 f a d f a2 c3 b2_8", [Dyn.f, Dyn.p]],
        ["s2l", "d3_8 g b_8.", [Dyn.p, Dyn.f]],
        ["l2s", "g3_16 e g c e g2 b a_8", [Dyn.f, Dyn.p]],
        ["s2s", "c3_8", [Dyn.mf]],
        ["l2s", "d3_16 f b2 d3 g2_8", [Dyn.mf, Dyn.f]],
        ["s2s", "b2_8", [Dyn.f]],
        ["l2s", "c3_16 e a2 c3 f2_8", [Dyn.f, Dyn.p]],
        ["s2s", "d2_8 g2_16", [Dyn.p, Dyn.mp]],
        ["l2s", "g3_16 f g c", [Dyn.mp, Dyn.mf]],
        ["l2s", "g3_16 c4 e d g3 d4 f e_8", [Dyn.mf, Dyn.f]]
    ]
    for fragment in lowervoice_fragments:
        lowervoice.append(ff(type=fragment[0],
                             nanonotation=fragment[1],
                             volumes=fragment[2]))
    p2m.add_phrases(uppervoice, start_time=0, track=0, channel=0)
    p2m.add_phrases(lowervoice, start_time=0, track=1, channel=0)
    p2m.set_tempo(86, 0)
    p2m.write(outputfile)


if __name__ == "__main__":
    play_bach()
