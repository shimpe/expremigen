import sys
import unittest

from expremigen.io.constants import Defaults, PhraseProperty as PP
from expremigen.io.phrase import Phrase
from expremigen.musicalmappings.durations import Durations as Dur
from expremigen.musicalmappings.dynamics import Dynamics as Dyn
from expremigen.musicalmappings.note2midi import Note2Midi
from expremigen.patterns.pconst import Pconst
from expremigen.patterns.pseq import Pseq
from expremigen.patterns.pseries import Pseries
from expremigen.patterns.ptween import Ptween


class TestPhrase(unittest.TestCase):
    def test_defaults(self):
        n = Note2Midi()
        p = Phrase()
        result = []
        for event in p:
            result.append(event)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][PP.NOTE], n.lookup(Defaults.note))
        self.assertEqual(result[0][PP.VOL], Defaults.vol)
        self.assertEqual(result[0][PP.DUR], 4 * Defaults.dur)
        self.assertEqual(result[0][PP.PLAYEDDUR], Defaults.playeddur)
        self.assertEqual(result[0][PP.LAG], Defaults.lag)
        self.assertEqual(result[0][PP.TEMPO], Defaults.tempo)

    def test_phrase(self):
        n = Note2Midi()
        properties = {
            PP.NOTE: Pseries(n.lookup("c4"), 1, 12),
            PP.VOL: Pconst(100, sys.maxsize),
            PP.DUR: Pconst(1 / 16, sys.maxsize),
            PP.PLAYEDDUR: Pconst(0.9, sys.maxsize),
            PP.LAG: Pconst(0, sys.maxsize)
        }
        p = Phrase(properties)
        result = []
        for event in p:
            result.append(event)
        self.assertEqual(len(result), 12)
        self.assertEqual(result[1][PP.NOTE], n.lookup("c#4"))
        self.assertEqual(result[5][PP.VOL], 100)
        self.assertEqual(result[9][PP.DUR], 4 * 0.0625)

    def test_phrase2(self):
        n = Note2Midi()
        notes = ["c4", "e4", "g4", "c5", "b4", "g4", "f4", "d4", "c4"]
        from vectortween.NumberAnimation import NumberAnimation
        from vectortween.SequentialAnimation import SequentialAnimation
        increase = NumberAnimation(frm=Dyn.mp, to=Dyn.f)
        decrease = NumberAnimation(frm=Dyn.f, to=Dyn.ppp)
        swell_dim = SequentialAnimation([increase, decrease])
        increasing_staccato = NumberAnimation(frm=1, to=0.8)
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
        result = []
        for event in p:
            result.append(event)
        self.assertEqual(len(result), 9)
        # check that last note longer
        self.assertEqual(result[7][PP.DUR], 4 * 1 / 4)
        self.assertEqual(result[8][PP.DUR], 4 * 1)
        # check that volume increases then decreases
        self.assertLess(result[0][PP.VOL], result[4][PP.VOL])
        self.assertLess(result[8][PP.VOL], result[4][PP.VOL])
        self.assertLess(result[8][PP.VOL], result[0][PP.VOL])
        # check that staccato increases
        for i in range(8):
            self.assertTrue(result[i][PP.PLAYEDDUR] > result[i + 1][PP.PLAYEDDUR])
        self.assertEqual(result[8][PP.NOTE], n.lookup("c4"))

    def test_cc(self):
        properties = {
            PP.NOTE: Pconst(67, 5),
            PP.DUR: Pconst(1 / 2, 5),
            "D35": Pconst(1 / 4, 10),
            "V35": Pseq([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10),
            "D34": Pconst(1 / 8, 20),
            "V34": Pseq([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 20)
        }
        p = Phrase(properties)
        result = []
        for event in p:
            result.append(event)
        self.assertEqual(len(result), 5 + 10 + 20)
        self.assertEqual(result[-2]["V35"], 9)
        self.assertEqual(result[-2]["D35"], 4 * 1 / 4)
        self.assertEqual(result[-12]["V34"], 19)
        self.assertEqual(result[-12]["D34"], 4 * 1 / 8)


if __name__ == '__main__':
    unittest.main()
