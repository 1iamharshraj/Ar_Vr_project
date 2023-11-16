import assemblyai as aai
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
from noisereduce import reduce_noise

def record_and_save(filename, duration=5, sample_rate=44100, noise_reduction=True):
    # Record audio
    print("Recording...")
    recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=2, dtype=np.int16)
    sd.wait()

    # Apply noise reduction
    if noise_reduction:
        print("Applying noise reduction...")
        recording = reduce_noise(audio_clip=np.array(recording), noise_clip=np.array(recording))

    # Convert to AudioSegment
    audio_data = np.array(recording, dtype=np.int16)
    audio_segment = AudioSegment(audio_data.tobytes(), frame_rate=sample_rate, sample_width=audio_data.dtype.itemsize, channels=2)

    # Save as MP3
    print(f"Saving recording to {filename}...")
    audio_segment.export(filename, format="mp3")
    print("Recording saved.")

if __name__ == "__main__":
    output_filename = "recorded_audio.mp3"
    recording_duration = 10  # Set the desired recording duration in seconds

    record_and_save(output_filename, duration=recording_duration, noise_reduction=True)


"""
# Replace with your API token
aai.settings.api_key = f"911437021fca4d599b54bd7a7d10c444"
#save_as_mp3(record_audio())
# URL of the file to transcribe
FILE_URL = "seeyouagain.mp3"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_URL)

print(transcript.text)
"""