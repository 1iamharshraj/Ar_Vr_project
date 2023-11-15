import whisper
import sounddevice as sd
from pydub import AudioSegment

def record_audio(duration=5, sample_rate=44100):
    # Record audio
    print("Recording")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait(1)

    # Convert NumPy array to AudioSegment
    audio_data = AudioSegment(
        recording.tobytes(),
        frame_rate=sample_rate,
        sample_width=recording.dtype.itemsize,
        channels=2
    )
    print("Recorded")

    return audio_data

def save_as_mp3(audio_data, output_filename='output.mp3', bitrate='192k'):
    # Save AudioSegment as MP3
    audio_data.export(output_filename, format="mp3", bitrate=bitrate)

def whisper_txt():
    model = whisper.load_model("base")

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio("output.mp3")
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)
    if('cat' or 'Cat' in result.text ):
        return 'cat'
    elif('wolf' or 'wolf' or 'subramani' or 'Subramani' in result.text):
        return 'wolf'
    else
        return None

