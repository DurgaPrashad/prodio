# tests/test_transcription.py
import unittest
from utils.transcription import AudioTranscriber
import os

class TestTranscription(unittest.TestCase):
    def setUp(self):
        self.transcriber = AudioTranscriber()
        # Create test audio file path
        self.test_audio_path = "test_audio.wav"
    
    def test_transcribe(self):
        # Skip if test file doesn't exist
        if not os.path.exists(self.test_audio_path):
            self.skipTest("Test audio file not found")
        
        result = self.transcriber.transcribe(self.test_audio_path)
        self.assertIsInstance(result, dict)
        self.assertIn('text', result)
        self.assertIn('language', result)
        self.assertIn('segments', result)