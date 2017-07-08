import unittest

from expremigen.patterns.pwhite import Pwhite


class TestPwhite(unittest.TestCase):
    def test_normal(self):
        a = [i for i in Pwhite(4, 5, 10)]
        # print(a)
        self.assertEqual(len(a), 10)

    def test_empty(self):
        a = [i for i in Pwhite(4, 5, 0)]
        self.assertEqual(a, [])

    def test_repr(self):
        self.assertEqual("{0}".format(Pwhite(0, 1.5, 4)), "Pwhite(0, 1.5, 4)")


if __name__ == '__main__':
    unittest.main()
