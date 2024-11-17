import os
import torch
import torchaudio
import pandas as pd
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from typing import List
import time
from tqdm import tqdm

class AudioProcessor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Use a public model that doesn't require authentication
        model_name = "facebook/wav2vec2-base"
        print(f"Loading model: {model_name}")
        
        try:
            self.processor = Wav2Vec2Processor.from_pretrained(model_name, local_files_only=False)
            self.model = Wav2Vec2ForCTC.from_pretrained(model_name).to(self.device)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise
        
        # Shorter chunks for faster processing
        self.sample_rate = 16000
        self.chunk_duration = 10  # reduced from 30 to 10 seconds
        self.chunk_length = self.chunk_duration * self.sample_rate
        
    def load_audio(self, audio_path: str) -> tuple:
        """Load and preprocess audio file"""
        print(f"Loading audio: {audio_path}")
        try:
            waveform, sample_rate = torchaudio.load(audio_path)
            
            # Convert to mono if stereo
            if waveform.shape[0] > 1:
                waveform = torch.mean(waveform, dim=0, keepdim=True)
            
            # Resample if needed
            if sample_rate != self.sample_rate:
                resampler = torchaudio.transforms.Resample(sample_rate, self.sample_rate)
                waveform = resampler(waveform)
            
            duration = len(waveform.squeeze()) / self.sample_rate
            print(f"Audio duration: {duration:.2f} seconds")
            return waveform.squeeze(), duration
        except Exception as e:
            print(f"Error loading audio file: {str(e)}")
            raise

    def process_audio(self, waveform: torch.Tensor, duration: float) -> List[str]:
        """Process audio in chunks and transcribe with progress bar"""
        transcriptions = []
        
        # Calculate number of chunks
        num_chunks = int(np.ceil(len(waveform) / self.chunk_length))
        
        # Process in chunks with progress bar
        with tqdm(total=num_chunks, desc="Processing chunks") as pbar:
            for i in range(0, len(waveform), self.chunk_length):
                chunk = waveform[i:i + self.chunk_length]
                
                # Skip chunks that are too short
                if len(chunk) < self.sample_rate:
                    continue
                    
                try:
                    # Prepare inputs
                    inputs = self.processor(
                        chunk.numpy(), 
                        sampling_rate=self.sample_rate, 
                        return_tensors="pt"
                    ).input_values.to(self.device)
                    
                    # Get predictions
                    with torch.no_grad():
                        logits = self.model(inputs).logits
                        predicted_ids = torch.argmax(logits, dim=-1)
                        transcription = self.processor.decode(predicted_ids[0])
                        transcriptions.append(transcription)
                        
                except Exception as e:
                    print(f"\nError processing chunk: {str(e)}")
                    continue
                
                pbar.update(1)
                
        return transcriptions

def main():
    # Set paths
    input_dir = "C:/Users/durga/OneDrive/Desktop/prodio working model/audio_files/Dataset"

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize processor
    try:
        processor = AudioProcessor()
    except Exception as e:
        print(f"Failed to initialize processor: {str(e)}")
        return
    
    results = []
    
    # Process each audio file
    for filename in os.listdir(input_dir):
        if filename.endswith(('.wav', '.mp3', '.m4a')):
            print(f"\nProcessing {filename}")
            file_path = os.path.join(input_dir, filename)
            
            try:
                # Track processing time
                start_time = time.time()
                
                # Load and process audio
                waveform, duration = processor.load_audio(file_path)
                print(f"Estimated processing time: {duration/5:.1f} to {duration/2:.1f} minutes")
                
                transcriptions = processor.process_audio(waveform, duration)
                
                # Combine transcriptions
                full_text = " ".join(transcriptions)
                
                # Calculate processing time
                process_time = time.time() - start_time
                
                results.append({
                    'file_name': filename,
                    'transcription': full_text,
                    'duration': duration,
                    'process_time': process_time,
                    'status': 'success'
                })
                print(f"Successfully processed {filename} in {process_time/60:.1f} minutes")
                
                # Save intermediate results
                df = pd.DataFrame(results)
                intermediate_file = os.path.join(output_dir, 'transcriptions_intermediate.csv')
                df.to_csv(intermediate_file, index=False)
                
            except Exception as e:
                print(f"Failed to process {filename}: {str(e)}")
                results.append({
                    'file_name': filename,
                    'transcription': '',
                    'duration': 0,
                    'process_time': 0,
                    'status': f'error: {str(e)}'
                })
    
    # Save final results
    if results:
        df = pd.DataFrame(results)
        output_file = os.path.join(output_dir, 'transcriptions_final.csv')
        df.to_csv(output_file, index=False)
        print(f"\nFinal results saved to {output_file}")
    else:
        print("\nNo results to save")

if __name__ == "__main__":
    import numpy as np
    main()