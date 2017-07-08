import unittest

from expremigen.patterns.pconst import Pconst


class TestPconst(unittest.TestCase):
    def test_normal(self):
        a = [i for i in Pconst(4, 10)]
        self.assertEqual(a, [4] * 10)

    def test_empty(self):
        b = [i for i in Pconst(4, 0)]
        self.assertEqual(b, [])

    def test_negative(self):
        c = [i for i in Pconst(-10, 100)]
        self.assertEqual(c, [-10] * 100)

    def test_adult(self):
        d = [i for i in Pconst("x", 3)]
        self.assertEqual(d, ["x"] * 3)

    def test_repr(self):
        self.assertEqual("{0}".format(Pconst(10, 3)), "Pconst(10, 3)")

    def test_defaultvalue(self):
        e = [i for i in Pconst(repeats=2)]
        self.assertEqual(e, [0, 0])


if __name__ == '__main__':
    unittest.main()
