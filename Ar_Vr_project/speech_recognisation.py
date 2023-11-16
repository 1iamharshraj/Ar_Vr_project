import assemblyai as aai
import sounddevice as sd
import soundfile as sf
from MarkerDetection_3dRendering import *
def record_3d():
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
    #reduced_audio = nr.reduce_noise(y=voice, sr=sample_rate)
    sf.write("output.wav", voice, sample_rate)

    # Play back the original audio
    print("Playing back the original recording...")
    sd.play(audio, sample_rate)
    sd.wait()

    # Play back the audio after noise reduction
    print("Playing back the processed recording...")
    sd.play(audio, sample_rate)
    sd.wait()

    aai.settings.api_key = f"911437021fca4d599b54bd7a7d10c444"
    #save_as_mp3(record_audio())
    # URL of the file to transcribe
    FILE_URL = "output.wav"

    # You can also transcribe a local file by passing in a file path
    # FILE_URL = './path/to/file.mp3'

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)

    print(transcript.text)
    temp = str(transcript.text)
    print(temp)
    if('cat' in temp or 'Cat' in temp):
        return 'cat'
    if('wolf' in temp):
        return 'wolf'
    else:
        return None

def animalTo3d(Animal_name):
    animal_dict = {'cat': r'cat.obj','wolf': r'wolf.obj'}
    Animal_name = Animal_name.casefold()
    path = animal_dict[Animal_name]
    return path

Animal = record_3d()
if Animal:
    main(animalTo3d(Animal))
else:
    print("The provided voice didnt have proper animal please try again")