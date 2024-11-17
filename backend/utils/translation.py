# utils/translation.py

from transformers import MBartForConditionalGeneration, MBartTokenizer
import torch

class Translator:
    def __init__(self):
        # Initialize model and tokenizer once
        self.model_name = "facebook/mbart-large-50-many-to-many-mmt"
        self.model = MBartForConditionalGeneration.from_pretrained(self.model_name)
        self.tokenizer = MBartTokenizer.from_pretrained(self.model_name)
        
        # Move to GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)

    def translate(self, text, source_lang="kn", target_lang="en_XX"):
        """
        Translate text from source language to target language
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language code (default: Kannada)
            target_lang (str): Target language code (default: English)
        
        Returns:
            str: Translated text
        """
        try:
            # Set source language
            self.tokenizer.src_lang = source_lang

            # Encode the text
            encoded = self.tokenizer(text, return_tensors="pt", padding=True)
            
            # Move input to same device as model
            encoded = {k: v.to(self.device) for k, v in encoded.items()}

            # Generate translation with better parameters
            generated_tokens = self.model.generate(
                **encoded,
                forced_bos_token_id=self.tokenizer.lang_code_to_id[target_lang],
                max_length=1024,
                num_beams=5,
                length_penalty=1.0,
                early_stopping=True
            )

            # Decode the translation
            translation = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

            return translation

        except Exception as e:
            print(f"Error in translation: {str(e)}")
            return f"Translation Error: {str(e)}"

    def get_supported_languages(self):
        """Return list of supported language pairs"""
        return {
            'Kannada': 'kn',
            'Hindi': 'hi_IN',
            'English': 'en_XX',
            'Tamil': 'ta_IN',
            'Telugu': 'te_IN',
            # Add more languages as needed
        }