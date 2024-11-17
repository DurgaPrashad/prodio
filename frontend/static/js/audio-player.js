
// static/js/audio-player.js
class AudioPlayer {
   constructor() {
       this.player = document.getElementById('audio-player');
       this.playBtn = document.getElementById('play-btn');
       this.prevBtn = document.getElementById('prev-btn');
       this.nextBtn = document.getElementById('next-btn');
       this.currentTrackIndex = 0;
       this.playlist = [];

       this.setupEventListeners();
   }

   setupEventListeners() {
       this.playBtn.addEventListener('click', () => this.togglePlay());
       this.prevBtn.addEventListener('click', () => this.playPrevious());
       this.nextBtn.addEventListener('click', () => this.playNext());
       
       this.player.addEventListener('play', () => {
           this.playBtn.textContent = '⏸';
       });
       
       this.player.addEventListener('pause', () => {
           this.playBtn.textContent = '▶';
       });

       this.player.addEventListener('ended', () => {
           this.playNext();
       });
   }

   setPlaylist(playlist) {
       this.playlist = playlist;
       this.updateControlsState();
   }

   async loadTrack(track) {
       if (!track) return;

       this.player.src = track.url;
       this.player.load();
       
       // Update active track in playlist UI
       document.querySelectorAll('.playlist-item').forEach(item => {
           item.classList.remove('active');
           if (item.dataset.id === track.id) {
               item.classList.add('active');
           }
       });

       // Load and display transcription and translation
       try {
           const transcription = await API.getTranscription(track.id);
           const translation = await API.getTranslation(track.id);
           
           document.getElementById('transcription-content').textContent = transcription.text;
           document.getElementById('translation-content').textContent = translation.text;
       } catch (error) {
           console.error('Error loading track details:', error);
       }
   }

   togglePlay() {
       if (this.player.paused) {
           this.player.play();
       } else {
           this.player.pause();
       }
   }

   playTrack(index) {
       if (index >= 0 && index < this.playlist.length) {
           this.currentTrackIndex = index;
           this.loadTrack(this.playlist[index]);
           this.player.play();
           this.updateControlsState();
       }
   }

   playNext() {
       if (this.currentTrackIndex < this.playlist.length - 1) {
           this.playTrack(this.currentTrackIndex + 1);
       }
   }

   playPrevious() {
       if (this.currentTrackIndex > 0) {
           this.playTrack(this.currentTrackIndex - 1);
       }
   }

   updateControlsState() {
       this.prevBtn.disabled = this.currentTrackIndex === 0;
       this.nextBtn.disabled = this.currentTrackIndex === this.playlist.length - 1;
   }
}