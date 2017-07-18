import unittest

from expremigen.musicalmappings.nanonotation import NanoNotation


class TestNanoNotation(unittest.TestCase):
    def test_notes(self):
        nn = NanoNotation()
        the_notes = nn.notes("r_8 c4 e4_16 f4_8.")
        self.assertEqual(the_notes, "r c4 e4 f4".split(" "))

    def test_durs(self):
        nn = NanoNotation()
        the_durs = nn.dur("r_8 c4 e4_16 f4_8.")
        self.assertEqual(the_durs, [1 / 8, 1 / 8, 1 / 16, 1 / 8 + 1 / 16])

    def test_octaves(self):
        nn = NanoNotation()
        the_notes = nn.notes("r_8 c3 e g4 a_2 e")
        self.assertEqual(the_notes, "r c3 e3 g4 a4 e4".split(" "))


if __name__ == '__main__':
    unittest.main()
