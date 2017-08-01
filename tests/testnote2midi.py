import unittest

from expremigen.musicalmappings.constants import REST
from expremigen.musicalmappings.note2midi import Note2Midi
from expremigen.patterns.pchord import Pchord


class TestNote2Midi(unittest.TestCase):
    def test_lookup(self):
        n = Note2Midi()
        self.assertEqual(n.lookup("a4"), 69)
        self.assertEqual(n.lookup("c4"), 60)
        self.assertEqual(n.lookup("bx3"), 61)
        self.assertEqual(n.lookup("c#4"), 61)
        self.assertEqual(n.lookup("db4"), 61)
        self.assertEqual(n.lookup("dbb3"), 48)
        self.assertEqual(n.lookup("b10"), REST)  # note number > 127 not allowed

    def test_map(self):
        n = Note2Midi()
        m = n.convert(["a4", "b4", "c5", "d5", "e5", "f5", "g#4", "f5", "e5", "d5", "UNKNOWN", "b4"])
        m2 = [i for i in m]
        expected = [69, 71, 72, 74, 76, 77, 68, 77, 76, 74, REST, 71]
        self.assertListEqual(m2, expected)

    def test_chord(self):
        n = Note2Midi()
        m = n.convert(["a3", Pchord(["c3", "e3", "g3"]), "d4"])
        m2 = [i for i in m]
        expected = [57, Pchord([48, 52, 55]), 62]
        self.assertEqual(m2, expected)
        q = n.convert2(["a3", Pchord(["c3", "e3", "g3"]), "d4"])
        q2 = [i for i in q]
        self.assertEqual(q2, expected)

    def test_drum(self):
        n = Note2Midi()
        m = n.convert(["openhihat", "ohh"])
        m2 = [i for i in m]
        expected = [46, 46]
        self.assertEqual(m2, expected)

if __name__ == '__main__':
    unittest.main()
