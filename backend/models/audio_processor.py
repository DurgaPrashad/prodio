# models/audio_processor.py
from utils.transcription import AudioTranscriber
from utils.translation import Translator
from utils.text_to_speech import TextToSpeech

class AudioProcessor:
    def __init__(self, file_path, upload_folder='uploads'):
        self.file_path = file_path
        self.transcriber = AudioTranscriber()
        self.translator = Translator()
        self.tts = TextToSpeech(upload_folder)
    
    def process(self):
        """Process audio file and return transcription, translation, and translated audio"""
        # Get transcription and translation
        result = self.transcriber.transcribe_and_translate(self.file_path)
        
        # Convert translated text to speech
        tts_result = self.tts.convert_to_speech(result['translated_text'])
        
        if tts_result['success']:
            result['translated_audio_path'] = tts_result['path']
        else:
            result['translated_audio_path'] = None
            
        return result