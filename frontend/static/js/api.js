// static/js/api.js

class API {
   // Base URL for the backend API
   static BASE_URL = 'http://localhost:5000/api';

   // Helper function to handle fetch requests
   static async request(endpoint, options = {}) {
       try {
           const response = await fetch(`${this.BASE_URL}${endpoint}`, options);
           if (!response.ok) {
               throw new Error(`HTTP error! Status: ${response.status}`);
           }
           return await response.json();
       } catch (error) {
           console.error(`API request to ${endpoint} failed:`, error);
           throw error;  // Re-throwing the error for further handling by calling function
       }
   }

   // Upload audio file to the server
   static async uploadAudio(file) {
       const formData = new FormData();
       formData.append('audio', file);

       // Using the helper function to send the request
       return this.request('/upload', {
           method: 'POST',
           body: formData,
       });
   }

   // Fetch the playlist from the server
   static async getPlaylist() {
       return this.request('/playlist');
   }

   // Fetch transcription for a specific file by its ID
   static async getTranscription(fileId) {
       return this.request(`/transcription/${fileId}`);
   }

   // Fetch translation for a specific file by its ID
   static async getTranslation(fileId) {
       return this.request(`/translation/${fileId}`);
   }
}

