class PlaylistManager {
   constructor(audioPlayer) {
       this.audioPlayer = audioPlayer;
       this.uploadBtn = document.getElementById('upload-btn');
       this.fileInput = document.getElementById('audio-upload');
       this.playlistContainer = document.getElementById('playlist');
       this.uploadProgress = document.getElementById('upload-progress'); // Progress bar container
       this.timeRemainingText = document.getElementById('time-remaining'); // Text for showing time remaining

       this.setupEventListeners();
       this.loadPlaylist();
   }

   setupEventListeners() {
       this.uploadBtn.addEventListener('click', () => {
           this.fileInput.click();
       });

       this.fileInput.addEventListener('change', async (event) => {
           if (event.target.files.length > 0) {
               const file = event.target.files[0];
               try {
                   this.uploadBtn.disabled = true;
                   this.uploadBtn.textContent = 'Uploading...';

                   // Show progress bar and time estimate
                   this.uploadProgress.style.display = 'block';
                   this.timeRemainingText.textContent = 'Estimating time...';

                   // Start file upload with progress
                   await this.uploadAudioWithProgress(file);

                   // After upload, load playlist and reset UI
                   await this.loadPlaylist();
                   this.uploadBtn.textContent = 'Upload Audio';
                   this.fileInput.value = '';

               } catch (error) {
                   console.error('Upload failed:', error);
                   alert('Upload failed. Please try again.');
               } finally {
                   this.uploadBtn.disabled = false;
                   this.uploadProgress.style.display = 'none';
               }
           }
       });
   }

   // Method to upload the audio with progress tracking
   async uploadAudioWithProgress(file) {
       return new Promise((resolve, reject) => {
           const formData = new FormData();
           formData.append('audio', file);

           const xhr = new XMLHttpRequest();
           xhr.open('POST', '/upload', true); // Replace with your API endpoint

           // Event listener for upload progress
           xhr.upload.addEventListener('progress', (event) => {
               if (event.lengthComputable) {
                   const percentage = (event.loaded / event.total) * 100;
                   document.getElementById('upload-progress-bar').value = percentage;

                   // Estimate time remaining based on upload speed
                   const elapsedTime = event.timeStamp / 1000; // Time in seconds
                   const speed = event.loaded / elapsedTime; // Bytes per second
                   const remainingTime = (event.total - event.loaded) / speed; // Estimate remaining time in seconds
                   this.updateTimeRemaining(remainingTime);
               }
           });

           xhr.onload = () => {
               if (xhr.status === 200) {
                   resolve();
               } else {
                   reject('Upload failed');
               }
           };

           xhr.onerror = () => {
               reject('Network error');
           };

           xhr.send(formData);
       });
   }

   // Method to update the remaining time on the UI
   updateTimeRemaining(remainingTime) {
       const minutes = Math.floor(remainingTime / 60);
       const seconds = Math.floor(remainingTime % 60);
       this.timeRemainingText.textContent = `Time remaining: ${minutes}m ${seconds}s`;
   }

   async loadPlaylist() {
       try {
           const playlist = await API.getPlaylist();
           this.audioPlayer.setPlaylist(playlist);
           this.renderPlaylist(playlist);
       } catch (error) {
           console.error('Failed to load playlist:', error);
       }
   }

   renderPlaylist(playlist) {
       this.playlistContainer.innerHTML = '';

       playlist.forEach((track, index) => {
           const item = document.createElement('div');
           item.className = 'playlist-item';
           item.dataset.id = track.id;
           item.textContent = track.name;

           item.addEventListener('click', () => {
               this.audioPlayer.playTrack(index);
           });

           this.playlistContainer.appendChild(item);
       });
   }
}
