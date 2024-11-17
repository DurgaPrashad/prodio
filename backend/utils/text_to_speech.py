# utils/text_to_speech.py
from gtts import gTTS
import os
import uuid

class TextToSpeech:
    def __init__(self, output_folder='uploads'):
        self.output_folder = output_folder
        
    def convert_to_speech(self, text, lang='en'):
        """Convert text to speech and save as audio file"""
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=lang, slow=False)
            
            # Generate unique filename
            audio_id = str(uuid.uuid4())
            output_path = os.path.join(self.output_folder, f"{audio_id}_translated.mp3")
            
            # Save to file
            tts.save(output_path)
            
            return {
                'success': True,
                'path': output_path,
                'id': audio_id
            }
        except Exception as e:
            print(f"Error in text to speech conversion: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }