import unittest

from expremigen.padd import Padd
from expremigen.pconst import Pconst
from expremigen.pseq import Pseq


class TestPadd(unittest.TestCase):
    def test_normal(self):
        a = [i for i in Padd(Pconst(4, 3), Pseq([1, 2, 3], 1))]
        self.assertEqual(a, [5, 6, 7])

    def test_firstlonger(self):
        a = [i for i in Padd(Pconst(4, 5), Pseq([1, 2, 3], 1))]
        self.assertEqual(a, [5, 6, 7])

    def test_secondlonger(self):
        a = [i for i in Padd(Pconst(4, 3), Pseq([1, 2, 3, 70], 1))]
        self.assertEqual(a, [5, 6, 7])

    def test_firstempty(self):
        a = [i for i in Padd(Pconst(4, 0), Pseq([1, 2, 3, 70], 1))]
        self.assertEqual(a, [])

    def test_secondempty(self):
        a = [i for i in Padd(Pconst(4, 3), Pseq([1, 2, 3, 70], 0))]
        self.assertEqual(a, [])

    def test_rightlazy(self):
        a = [i for i in Padd(Pconst(4, 3), Pseq([1, 2, 3, 70], int(5e5)))]
        self.assertEqual(a, [5, 6, 7])

    def test_leftlazy(self):
        a = [i for i in Padd(Pconst(4, int(5e8)), Pseq([1, 2, 3, 70], 2))]
        self.assertEqual(a, [5, 6, 7, 74, 5, 6, 7, 74])

    def test_repr(self):
        tested = "{0}".format(Padd(Pconst(4, 5), Pseq([1, 2, 3], 1)))
        expected = "Padd(Pconst(4, 5), Pseq([1, 2, 3], 1))"
        self.assertEqual(tested, expected)


if __name__ == '__main__':
    unittest.main()
