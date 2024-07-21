import os
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEEPGRAM_API_KEY = os.environ['DEEPGRAM_API_KEY']

def transcribe_file(file_path):
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    with open(file_path, 'rb') as audio:
        buffer_data = audio.read()

    payload: FileSource = {
        'buffer': buffer_data,
    }

    options = PrerecordedOptions(
        model="nova-2",
        smart_format=True,
    )

    try:
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        return response["results"]["channels"][0]["alternatives"][0]["transcript"]
    except Exception as e:
        print(f"Exception: {e}")
        return None
