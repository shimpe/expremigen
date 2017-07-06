import unittest

from expremigen.pseq import Pseq


class TestPseq(unittest.TestCase):
    def test_normal(self):
        a = [i for i in Pseq([4, 5, 6], 2)]
        self.assertEqual(a, [4, 5, 6] * 2)

    def test_empty(self):
        b = [i for i in Pseq([4, 5, 6], 0)]
        self.assertEqual(b, [])

    def test_adult(self):
        d = [i for i in Pseq(["X", "Y", "X"], 3)]
        self.assertEqual(d, ["X", "Y", "X"] * 3)

    def test_repr(self):
        self.assertEqual("{0}".format(Pseq([1, -1, 2], 3)), "Pseq([1, -1, 2], 3)")

    def test_defaultvalue(self):
        e = [i for i in Pseq(repeats=2)]
        self.assertEqual(e, [])


if __name__ == '__main__':
    unittest.main()
