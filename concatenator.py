from pydub import AudioSegment
import os
import re

AudioSegment.converter = "C:/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"

# Specify the input folder and output file
input_folder = "input_audio"  # Folder containing audio files to concatenate
output_file = "outro.mp3"  # Output file name


# Function to concatenate audio files in segments to avoid memory issues
def concatenate_audios_in_segments(input_folder, output_file, segment_size=60 * 60 * 1000):
    # Get a list of all audio files in the input folder
    audio_files = [file for file in os.listdir(input_folder) if file.endswith(('.mp3', '.wav'))]

    # Sort the files numerically based on the chunk number
    audio_files.sort(key=lambda x: int(re.search(r'output_chunk_(\d+)\.mp3', x).group(1)))
    # Alternatively:
    # audio_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

    if not audio_files:
        print("No audio files found in the specified folder.")
        return

    combined_audio = AudioSegment.empty()  # Initialize an empty AudioSegment

    # Process and combine each audio file in segments
    for file in audio_files:
        audio = AudioSegment.from_file(os.path.join(input_folder, file))
        combined_audio += audio

        # If the combined audio exceeds the segment size, export it and reset
        if len(combined_audio) >= segment_size:
            # Export the current segment
            segment_file = f"segment_{audio_files.index(file)}.mp3"
            combined_audio.export(segment_file, format="mp3")
            print(f"Saved segment: {segment_file}")
            combined_audio = AudioSegment.empty()  # Reset the combined audio

    # Export any remaining audio
    if len(combined_audio) > 0:
        combined_audio.export(output_file, format="mp3")
        print(f"Final concatenated audio saved to {output_file}")


# Run the concatenation function
concatenate_audios_in_segments(input_folder, output_file)
