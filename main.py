# Import the TTS library from Coqui
from TTS.api import TTS
import torch
import os
import re

# Check if GPU is available and display CUDA details
print("GPU Available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("CUDA Version:", torch.version.cuda)
    print("GPU Name:", torch.cuda.get_device_name(0))
else:
    print("Running on CPU.")

# Initialize the TTS model with GPU support
tts = TTS("tts_models/en/vctk/vits")  # Multi-speaker model
tts.to('cuda' if torch.cuda.is_available() else 'cpu')

# Get the list of available speakers
available_speakers = tts.speakers
if not available_speakers:
    print("No pre-trained speakers available in this model.")
    exit()

print("Available speakers:", available_speakers)

# Choose a speaker from the list
chosen_speaker = 'p311'  # Replace with your desired speaker ID
if chosen_speaker not in available_speakers:
    print(f"Chosen speaker '{chosen_speaker}' not found in the available speakers.")
    exit()

print("Chosen speaker:", chosen_speaker)

# Input folder for generated audio chunks
input_folder = "input_audio"

# Create the input folder if it doesn't exist
if not os.path.exists(input_folder):
    os.makedirs(input_folder)
    print(f"Created folder '{input_folder}'.")

# Function to sanitize text
def sanitize_text(text):
    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to split large text into manageable chunks
def split_text(text, max_length=249):
    chunks = []
    sentences = re.split(r'(?<=[.!?]) +', text)  # Split text into sentences

    for sentence in sentences:
        if len(sentence) <= max_length:
            chunks.append(sentence)
        else:
            # Split by words if the sentence is too long
            words = sentence.split(" ")
            current_chunk = []
            current_length = 0

            for word in words:
                if current_length + len(word) + 1 <= max_length:
                    current_chunk.append(word)
                    current_length += len(word) + 1
                else:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = [word]
                    current_length = len(word) + 1

            if current_chunk:
                chunks.append(" ".join(current_chunk))

    # Remove any empty chunks
    return [chunk for chunk in chunks if chunk.strip()]

# Load the large text from a file
text_file_path = "large_text_file.txt"
if not os.path.exists(text_file_path):
    print(f"File '{text_file_path}' not found. Please create it and add your text.")
    exit()

with open(text_file_path, "r", encoding="utf-8") as file:
    text = file.read()

# Sanitize and split the text into chunks to avoid memory issues
text = sanitize_text(text)
text_chunks = split_text(text)

# Iterate over chunks and generate speech for each, saving to separate MP3 files
for i, chunk in enumerate(text_chunks):
    # Ensure the chunk is within the character limit
    chunk = sanitize_text(chunk)
    output_file = f"{input_folder}/output_chunk_{i + 1}.mp3"

    try:
        # Generate speech using the chosen speaker
        tts.tts_to_file(text=chunk, file_path=output_file, speaker=chosen_speaker)
        print(f"Saved: {output_file}")
    except IndexError as e:
        print(f"IndexError for chunk {i}: {e}")
    except Exception as e:
        print(f"Error processing chunk {i}: {e}")

print("Text-to-speech conversion completed successfully!")
