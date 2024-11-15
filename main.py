# Import the TTS library from Coqui
from TTS.api import TTS
import torch
import os

print(torch.cuda.is_available())
print(torch.version.cuda)
print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU found")

# Initialize the TTS model with GPU support
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

tts.to('cuda')

# Specify the language for text-to-speech generation
language = "en"  # Change this to the desired language code (e.g., "es" for Spanish, "de" for German, etc.)

# Path to the reference audio file for speaker selection
speaker_reference = "C:/Users/help2/Downloads/teresea.wav"  # Update this with your reference file
input_folder = "input_audio"


# Create the input folder if it doesn't exist
if not os.path.exists(input_folder):
    os.makedirs(input_folder)
    print(f"Created folder '{input_folder}'. Please add your audio files to this folder and rerun the script.")

# Function to split large text into manageable chunks
def split_text(text, max_length=249):
    import re
    chunks = []
    sentences = re.split(r'(?<=[.!?]) +', text)  # Split text into sentences

    for sentence in sentences:
        if len(sentence) <= max_length:
            chunks.append(sentence)
        else:
            # Split by commas if the sentence is too long
            parts = sentence.split(", ")
            for part in parts:
                if len(part) <= max_length:
                    chunks.append(part)
                else:
                    # Split by words if the part is still too long
                    words = part.split(" ")
                    current_chunk = []
                    current_length = 0

                    for word in words:
                        if current_length + len(word) + 1 <= max_length:
                            current_chunk.append(word)
                            current_length += len(word) + 1
                        else:
                            # Save the current chunk and start a new one
                            chunks.append(" ".join(current_chunk))
                            current_chunk = [word]
                            current_length = len(word) + 1

                    if current_chunk:
                        chunks.append(" ".join(current_chunk))

    return chunks

# Load the large text from a file
with open("large_text_file.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Split the text into chunks to avoid memory issues
text_chunks = split_text(text)

# Iterate over chunks and generate speech for each, saving to separate MP3 files
for i, chunk in enumerate(text_chunks):
    output_file = f"input_audio/output_chunk_{i + 1}.mp3"
    tts.tts_to_file(text=chunk, file_path=output_file, language=language, speaker_wav=speaker_reference)
    print(f"Saved: {output_file}")

print("Text-to-speech conversion completed successfully!")
