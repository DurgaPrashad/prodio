# services/file_service.py
import os
import uuid
from werkzeug.utils import secure_filename

class FileService:
    def __init__(self, upload_folder, allowed_extensions):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions
        
        # Create upload folder if it doesn't exist
        os.makedirs(upload_folder, exist_ok=True)
    
    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def save_file(self, file):
        """Save uploaded file and return file details"""
        if file and self.allowed_file(file.filename):
            # Generate unique filename
            file_id = str(uuid.uuid4())
            filename = secure_filename(file.filename)
            extension = filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{file_id}.{extension}"
            
            # Save file
            file_path = os.path.join(self.upload_folder, unique_filename)
            file.save(file_path)
            
            return {
                'id': file_id,
                'filename': filename,
                'path': file_path
            }
        return None