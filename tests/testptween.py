import unittest

from vectortween.NumberAnimation import NumberAnimation

from expremigen.patterns.ptween import Ptween


class TestPtween(unittest.TestCase):
    def test_normal(self):
        n = NumberAnimation(frm=60, to=90, tween=['linear'])
        a = [i for i in Ptween(n, 0, 0, 10, 10, None)]
        self.assertEqual(a, [60, 63, 66, 69, 72, 75, 78, 81, 84, 87])

    def test_repr(self):
        n = NumberAnimation(frm=60, to=90, tween=['linear'])
        self.assertEqual("{0}".format(Ptween(n, 0, 0, 10, 10)), "Ptween(<anim>, 0, 0, 10, 10, None)")


if __name__ == '__main__':
    unittest.main()
