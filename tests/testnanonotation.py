import unittest

from expremigen.musicalmappings.nanonotation import NanoNotation
from expremigen.musicalmappings.note2midi import Note2Midi


class TestNanoNotation(unittest.TestCase):
    def test_notes(self):
        n = Note2Midi()
        nn = NanoNotation()
        the_notes = nn.notes("r_8 c4 e4_16 f4_8.")
        self.assertEqual(the_notes, n.convert2("r c4 e4 f4".split(" ")))

    def test_durs(self):
        nn = NanoNotation()
        the_durs = nn.dur("r_8 c4 e4_16 f4_8.")
        self.assertEqual(the_durs, [1 / 8, 1 / 8, 1 / 16, 1 / 8 + 1 / 16])


if __name__ == '__main__':
    unittest.main()
