import unittest

from expremigen.io.constants import PhraseProperty as PP
from expremigen.io.pat2midi import Pat2Midi
from expremigen.io.phrase import Phrase
from expremigen.musicalmappings.durations import Durations as Dur
from expremigen.musicalmappings.dynamics import Dynamics as Dyn
from expremigen.musicalmappings.note2midi import Note2Midi
from expremigen.patterns.pconst import Pconst


class TestPat2Midi(unittest.TestCase):
    def test_addPhrase(self):
        n = Note2Midi()
        properties = {
            PP.NOTE: Pconst(n.lookup("f#3"), 3),
            PP.VOL: Pconst(Dyn.mf),
            PP.DUR: Pconst(Dur.quarter),
            PP.PLAYEDDUR: Pconst(0.9),
            PP.LAG: Pconst(0)
        }
        p = Phrase(properties)
        p2m = Pat2Midi()
        duration = p2m.add_phrase(p)
        self.assertEqual(duration, 3 * 4 * Dur.quarter)
        duration2 = p2m.add_phrase(p, start_time=duration)
        # just adding a single phrase returns the duration of that phrase only
        self.assertEqual(duration, duration2)
        # adding a list of phrases returns the total duration
        total_duration = p2m.add_phrases([p], start_time=duration + duration2)
        self.assertEqual(total_duration, 3 * duration)


if __name__ == '__main__':
    unittest.main()
