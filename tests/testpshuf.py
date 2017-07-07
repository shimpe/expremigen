import unittest

from expremigen.pshuf import Pshuf


class TestPseq(unittest.TestCase):
    def test_normal(self):
        a = [i for i in Pshuf([4, 5, 6], 10)]
        self.assertCountEqual(a, [4, 5, 6] * 10)
        self.assertNotEqual(a, [4, 5, 6] * 10)

    def test_empty(self):
        b = [i for i in Pshuf([4, 5, 6], 0)]
        self.assertEqual(b, [])

    def test_repr(self):
        self.assertEqual("{0}".format(Pshuf([1, -1, 2], 3)), "Pshuf([1, -1, 2], 3)")


if __name__ == '__main__':
    unittest.main()
