

# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}
    DATABASE = os.path.join('instance', 'audio_files.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
