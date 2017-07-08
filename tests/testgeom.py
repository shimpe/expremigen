import unittest

from expremigen.patterns.pgeom import Pgeom


class TestPgeom(unittest.TestCase):
    def test_normal(self):
        a = [i for i in Pgeom(1, 10, 5)]
        self.assertEqual(a, [1, 10, 100, 1000, 10000])

    def test_negativestep(self):
        a = [i for i in Pgeom(1, -10, 5)]
        self.assertEqual(a, [1, -10, 100, -1000, 10000])

    def test_stepzero(self):
        a = [i for i in Pgeom(1, 0, 5)]
        self.assertEqual(a, [1, 0, 0, 0, 0])

    def test_zerolength(self):
        a = [i for i in Pgeom(0, 10, 0)]
        self.assertEqual(a, [])

    def test_repr(self):
        self.assertEqual("{0}".format(Pgeom(0, 10, 5)), "Pgeom(0, 10, 5)")


if __name__ == '__main__':
    unittest.main()
