import unittest

from expremigen.patterns.pexprand import Pexprand


class TestPexprand(unittest.TestCase):
    def test_normal(self):
        a = [i for i in Pexprand(4, 5, 10)]
        # print(a)
        self.assertEqual(len(a), 10)
        for i in range(10):
            self.assertTrue(4 < a[i] < 5)

    def test_negative(self):
        a = [i for i in Pexprand(-4, -5, 10)]
        # print(a)
        self.assertEqual(len(a), 10)
        for i in range(10):
            self.assertTrue(-5 < a[i] < -4)

    def test_empty(self):
        a = [i for i in Pexprand(4, 5, 0)]
        self.assertEqual(a, [])

    def test_repr(self):
        self.assertEqual("{0}".format(Pexprand(0.1, 1.5, 4)), "Pexprand(0.1, 1.5, 4)")


if __name__ == '__main__':
    unittest.main()
