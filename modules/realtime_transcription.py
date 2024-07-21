from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
import os

DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

def start_realtime_transcription(websocket):
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)
    dg_connection = deepgram.listen.live.v("1")

    def on_message(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        websocket.send(transcript)

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(
        model="nova-2",
        language="en-US",
        smart_format=True,
    )

    dg_connection.start(options)
    return dg_connection

def stop_realtime_transcription(dg_connection):
    dg_connection.finish()