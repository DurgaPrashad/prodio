# tests/test_translation.py
import unittest
from utils.translation import Translator

class TestTranslation(unittest.TestCase):
    def setUp(self):
        self.translator = Translator()
    
    def test_translate(self):
        test_text = "ನಮಸ್ಕಾರ"  # "Hello" in Kannada
        result = self.translator.translate(test_text)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, test_text)