import unittest

from expremigen.patterns.pchord import Pchord
from expremigen.patterns.pconst import Pconst
from expremigen.patterns.pseq import Pseq


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
        self.assertEqual("{0}".format(Pseq([1, -1, Pconst(2, 2)], 3)), "Pseq([1, -1, Pconst(2, 2)], 3)")

    def test_defaultvalue(self):
        e = [i for i in Pseq(repeats=2)]
        self.assertEqual(e, [])

    def test_nesting(self):
        f = [i for i in Pseq([Pseq([1, Pconst(2, 2)], 2), Pseq([3, 4], 2)], 2)]
        self.assertEqual(f, [1, 2, 2, 1, 2, 2, 3, 4, 3, 4, 1, 2, 2, 1, 2, 2, 3, 4, 3, 4])

    def test_withchord(self):
        f = [i for i in Pseq([Pseq([1, Pconst(2, 2)], 2), Pseq(Pchord([3, 4]), 2)], 2)]
        self.assertEqual(f, [1, 2, 2, 1, 2, 2, Pchord([3, 4]), Pchord([3, 4]), 1, 2, 2, 1, 2, 2, Pchord([3, 4]),
                             Pchord([3, 4])])


if __name__ == '__main__':
    unittest.main()
