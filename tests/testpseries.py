import unittest

from expremigen.patterns.pseries import Pseries


class TestPseries(unittest.TestCase):
    def test_normal(self):
        a = [i for i in Pseries(0, 10, 5)]
        self.assertEqual(a, [0, 10, 20, 30, 40])

    def test_negativestep(self):
        a = [i for i in Pseries(0, -10, 5)]
        self.assertEqual(a, [0, -10, -20, -30, -40])

    def test_stepzero(self):
        a = [i for i in Pseries(0, 0, 5)]
        self.assertEqual(a, [0, 0, 0, 0, 0])

    def test_zerolength(self):
        a = [i for i in Pseries(0, 10, 0)]
        self.assertEqual(a, [])

    def test_repr(self):
        self.assertEqual("{0}".format(Pseries(0, 10, 5)), "Pseries(0, 10, 5)")


if __name__ == '__main__':
    unittest.main()
