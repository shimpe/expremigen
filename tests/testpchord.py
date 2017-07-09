import unittest

from expremigen.patterns.pchord import Pchord


class TestPchord(unittest.TestCase):
    def test_normal(self):
        a = [i for i in Pchord(["a4", "c#5", "e5"])]
        self.assertEqual(a[0].notes, ["a4", "c#5", "e5"])

if __name__ == '__main__':
    unittest.main()
