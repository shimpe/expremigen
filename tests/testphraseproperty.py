import unittest

from expremigen.io.constants import PhraseProperty


class TestPrand(unittest.TestCase):
    def test_phraseproperty(self):
        self.assertEqual(PhraseProperty.CtrlValKey(45), "V45")
        self.assertEqual(PhraseProperty.CtrlDurKey(67), "D67")


if __name__ == '__main__':
    unittest.main()
