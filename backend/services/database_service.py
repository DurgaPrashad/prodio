import sqlite3

class DatabaseService:
    def __init__(self, database_url):
        # Initialize with the provided database URL
        self.database_url = database_url

    def init_db(self):
        """Initialize the database and create the required table."""
        with sqlite3.connect(self.database_url) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS audio_files (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    path TEXT NOT NULL,
                    transcription TEXT,
                    translation TEXT,
                    translated_audio_path TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def save_audio_file(self, file_id, filename, file_path, transcription, translation, translated_audio_path=None):
        """Save an audio file entry in the database."""
        with sqlite3.connect(self.database_url) as conn:
            conn.execute(
                '''INSERT INTO audio_files 
                   (id, name, path, transcription, translation, translated_audio_path) 
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (file_id, filename, file_path, transcription, translation, translated_audio_path)
            )
