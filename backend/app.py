from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from config import Config
from services.database_service import DatabaseService
from services.file_service import FileService
from models.audio_processor import AudioProcessor

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Load app configuration
app.config.from_object(Config)

# Initialize services
db_service = DatabaseService(Config.DATABASE)
file_service = FileService(Config.UPLOAD_FOLDER, Config.ALLOWED_EXTENSIONS)

# Initialize the database schema
db_service.init_db()

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handles file upload, processing, and saving to the database."""
    
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    
    if not file.filename:
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the file
    file_info = file_service.save_file(file)
    if not file_info:
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Process the audio file
    processor = AudioProcessor(file_info['path'], app.config['UPLOAD_FOLDER'])
    result = processor.process()
    
    # Save file details and processing results to the database
    db_service.save_audio_file(
        file_info['id'],
        file_info['filename'],
        file_info['path'],
        result['original_text'],
        result['translated_text'],
        result.get('translated_audio_path')
    )
    
    # Prepare the response with relevant URLs and transcription/translation
    return jsonify({
        'id': file_info['id'],
        'name': file_info['filename'],
        'url': f'/api/audio/{file_info["id"]}',
        'transcription': result['original_text'],
        'translation': result['translated_text'],
        'translated_audio_url': f'/api/translated-audio/{file_info["id"]}' if result.get('translated_audio_path') else None,
        'message': 'File processed successfully'
    }), 201

@app.route('/api/audio/<file_id>', methods=['GET'])
def get_audio(file_id):
    """Fetch the original audio file based on the provided file ID."""
    
    file_info = db_service.get_audio_file(file_id)
    if file_info:
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            os.path.basename(file_info[2])  # file_info[2] is the path
        )
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/transcription/<file_id>', methods=['GET'])
def get_transcription(file_id):
    """Fetch the transcription of the audio file."""
    
    file_info = db_service.get_audio_file(file_id)
    if file_info:
        return jsonify({'text': file_info[3]})  # file_info[3] is transcription
    return jsonify({'error': 'Transcription not found'}), 404

@app.route('/api/translation/<file_id>', methods=['GET'])
def get_translation(file_id):
    """Fetch the translation of the audio file."""
    
    file_info = db_service.get_audio_file(file_id)
    if file_info:
        return jsonify({'text': file_info[4]})  # file_info[4] is translation
    return jsonify({'error': 'Translation not found'}), 404

@app.route('/api/translated-audio/<file_id>', methods=['GET'])
def get_translated_audio(file_id):
    """Fetch the translated audio file."""
    
    file_info = db_service.get_audio_file(file_id)
    if file_info and file_info[5]:  # file_info[5] is translated_audio_path
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            os.path.basename(file_info[5])
        )
    return jsonify({'error': 'Translated audio not found'}), 404

@app.route('/api/playlist', methods=['GET'])
def get_playlist():
    """Fetch the playlist of all uploaded audio files."""
    
    files = db_service.get_playlist()
    playlist = [{
        'id': file[0],
        'name': file[1],
        'url': f'/api/audio/{file[0]}'
    } for file in files]
    
    return jsonify(playlist)

if __name__ == '__main__':
    app.run(debug=True)
