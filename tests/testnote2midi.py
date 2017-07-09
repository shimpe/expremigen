import unittest

from expremigen.musicalmappings.constants import REST
from expremigen.musicalmappings.note2midi import Note2Midi


class TestNote2Midi(unittest.TestCase):
    def test_lookup(self):
        n = Note2Midi()
        self.assertEqual(n.lookup("a4"), 69)
        self.assertEqual(n.lookup("c4"), 60)
        self.assertEqual(n.lookup("bx4"), 61)
        self.assertEqual(n.lookup("c#4"), 61)
        self.assertEqual(n.lookup("db4"), 61)
        self.assertEqual(n.lookup("dbb3"), 48)

    def test_map(self):
        n = Note2Midi()
        m = n.convert(["a4", "b4", "c5", "d5", "e5", "f5", "g#4", "f5", "e5", "d5", "UNKNOWN", "b4"])
        m2 = [i for i in m]
        expected = [69, 71, 72, 74, 76, 77, 68, 77, 76, 74, REST, 71]
        self.assertListEqual(m2, expected)


if __name__ == '__main__':
    unittest.main()
