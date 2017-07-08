import unittest

from expremigen.patterns.prand import Prand


class TestPrand(unittest.TestCase):
    def test_shorter(self):
        a = [i for i in Prand([4, 5, 6], 2)]
        self.assertEqual(len(a), 2)

    def test_longer(self):
        b = [i for i in Prand([4, 5, 6], 10)]
        self.assertEqual(len(b), 10)

    def test_repr(self):
        self.assertEqual("{0}".format(Prand([1, -1, 2], 3)), "Prand([1, -1, 2], 3)")


if __name__ == '__main__':
    unittest.main()
