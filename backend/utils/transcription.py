# utils/transcription.py

import whisper
import torch

class AudioTranscriber:
    def __init__(self):
        # Initialize Whisper model
        self.model = whisper.load_model("medium")  # Using medium model for better accuracy
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def transcribe(self, audio_path):
        """
        Transcribe audio file with specific handling for Kannada
        
        Args:
            audio_path (str): Path to audio file
            
        Returns:
            dict: Contains transcribed text and detected language
        """
        try:
            # Transcribe with specific settings for Kannada
            result = self.model.transcribe(
                audio_path,
                language="kn",  # Specify Kannada language
                task="transcribe",
                fp16=False,  # Disable half-precision to avoid potential errors
                initial_prompt="ಕನ್ನಡ ಭಾಷೆಯಲ್ಲಿ"  # Prompt in Kannada to improve recognition
            )

            return {
                'text': result['text'],
                'language': result['language'],
                'segments': result['segments']
            }

        except Exception as e:
            print(f"Error in transcription: {str(e)}")
            return {
                'text': f"Transcription Error: {str(e)}",
                'language': 'unknown',
                'segments': []
            }

    def transcribe_and_translate(self, audio_path):
        """
        Transcribe and translate in one step
        
        Args:
            audio_path (str): Path to audio file
            
        Returns:
            dict: Contains original transcription and English translation
        """
        # First transcribe
        transcription = self.transcribe(audio_path)
        
        # Then translate
        translator = Translator()
        translation = translator.translate(transcription['text'])

        return {
            'original_text': transcription['text'],
            'translated_text': translation,
            'detected_language': transcription['language']
        }