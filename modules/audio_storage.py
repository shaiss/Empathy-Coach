import os
from datetime import datetime

AUDIO_STORAGE_DIR = 'audio_storage'

def save_audio(audio_data, file_name=None):
    if not os.path.exists(AUDIO_STORAGE_DIR):
        os.makedirs(AUDIO_STORAGE_DIR)

    if file_name is None:
        file_name = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"

    file_path = os.path.join(AUDIO_STORAGE_DIR, file_name)

    with open(file_path, 'wb') as f:
        f.write(audio_data)

    return file_path

def get_audio(file_name):
    file_path = os.path.join(AUDIO_STORAGE_DIR, file_name)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return f.read()
    else:
        return None