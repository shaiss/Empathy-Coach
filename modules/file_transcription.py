import os
import logging
from deepgram import DeepgramClient, FileSource, PrerecordedOptions
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEEPGRAM_API_KEY = os.environ['DEEPGRAM_API_KEY']

# Set up logging
logger = logging.getLogger(__name__)

def transcribe_file(file):
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    payload: FileSource = {
        'buffer': file.read(),
        'mimetype': file.content_type
    }

    options = PrerecordedOptions(
        model="nova-2",
        smart_format=True,
        punctuate = True,
    )

    try:
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        logger.info(f"Deepgram API response: {response}")
        return response["results"]["channels"][0]["alternatives"][0]["transcript"]

    except Exception as e:
        logger.error(f"Exception in transcribe_file: {e}")
        raise
