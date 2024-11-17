import pandas as pd
print(pd.__version__)
from gtts import gTTS
import os

# Input and output file paths
input_csv = "../prodio working model/output/transcriptions_intermediate.csv"
output_folder = "mp3_output"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the CSV file
df = pd.read_csv(input_csv)

# Assuming the transcription column is named 'text'
for index, row in df.iterrows():
    text = row['text']
    filename = os.path.join(output_folder, f"audio_{index + 1}.mp3")
    
    try:
        # Convert text to speech
        tts = gTTS(text, lang='en')
        # Save the audio file
        tts.save(filename)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Error converting text at row {index + 1}: {e}")

print(f"All MP3 files saved in the folder: {output_folder}")
