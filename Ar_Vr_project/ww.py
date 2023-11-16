import sounddevice as sd
import numpy as np
import noisereduce as nr

# Constants for audio recording
sample_rate = 44100  # Sample rate in Hz
duration = 5  # Duration of the recording in seconds
threshold = 0.02  # Threshold to distinguish voice from noise

# Record audio
print("Recording...")
audio = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1)
sd.wait()

# Convert audio to mono
audio_mono = np.mean(audio, axis=1)

# Extract voice by applying noise thresholding
voice = audio_mono * (audio_mono > threshold)

# Apply noise reduction
reduced_audio = nr.reduce_noise(y=voice, sr=sample_rate)

# Play back the original audio
print("Playing back the original recording...")
sd.play(audio, sample_rate)
sd.wait()

# Play back the audio after noise reduction
print("Playing back the processed recording...")
sd.play(reduced_audio, sample_rate)
sd.wait()
