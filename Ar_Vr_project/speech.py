
import sounddevice as sd
from pydub import AudioSegment
import assemblyai as aai




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