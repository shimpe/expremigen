import unittest

from expremigen.io.constants import PhraseProperty


class TestPrand(unittest.TestCase):
    def test_phraseproperty(self):
        self.assertEqual(PhraseProperty.ctrl_val_key(45), "V45")
        self.assertEqual(PhraseProperty.ctrl_dur_key(67), "D67")


if __name__ == '__main__':
    unittest.main()
