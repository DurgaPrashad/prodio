# Audio Translation System

A web application for translating Kannada audio files to English text using AI models.
![image](https://github.com/user-attachments/assets/82b4533a-df11-4308-a250-5f63dbe5c3ad)

## Features

- Audio file upload and management
- Kannada speech recognition using Whisper
- Text translation from Kannada to English using MBart
- Dynamic playlist management
- Real-time audio playback
- Persistent storage of transcriptions and translations

## Requirements

- Python 3.8+
- Flask
- PyTorch
- Transformers
- Whisper
- SQLite3
- Node.js (optional, for development)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/audio-translation-project.git
cd audio-translation-project
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the environment variables:
```bash
cp .env.template .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Start the backend server:
```bash
flask run
```

6. Start the frontend (in a new terminal):
```bash
cd frontend
python -m http.server 8080
```

## Docker Setup

To run with Docker:

```bash
docker-compose up --build
```

## Usage

1. Access the application at `http://localhost:8080`
2. Upload Kannada audio files using the upload button
3. Wait for processing (transcription and translation)
4. View results in the interface

## Project Structure

The project follows a clear separation of concerns:

- `frontend/`: Contains all frontend assets
- `backend/`: Contains the Flask application
  - `models/`: Database and processing models
  - `utils/`: Utility functions
  - `services/`: Business logic
  - `uploads/`: Storage for uploaded files

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

Follow for More projects

## License

This project is licensed under the MIT License - see the LICENSE file for details.
