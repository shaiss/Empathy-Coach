import os
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO

from modules.audio_analysis import analyze_audio
from modules.data_integration import integrate_data
from modules.llm_integration import analyze_with_llm
from modules.text_analysis import analyze_text
from modules import realtime_transcription, file_transcription, audio_storage, feedback_generation, database
from modules.logger import setup_logger

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
socketio = SocketIO(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
db = database.get_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger.error('No file part in the request')
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        logger.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            file_path = audio_storage.save_audio(file.read(), file.filename)
            transcript = file_transcription.transcribe_file(file_path)

            # Perform empathy analysis
            audio_features = analyze_audio(file_path)
            text_features = analyze_text(transcript)
            integrated_data = integrate_data(audio_features, text_features)
            llm_analysis = analyze_with_llm(integrated_data)
            feedback = feedback_generation.generate_feedback(llm_analysis)

            # Save results to database
            result_id = database.save_result(db, file.filename, transcript, feedback)

            logger.info(f'Successfully processed file: {file.filename}')
            return jsonify({
                'transcript': transcript,
                'analysis': feedback,
                'result_id': result_id
            })
        except Exception as e:
            logger.error(f'Error processing file: {str(e)}')
            return jsonify({'error': 'An error occurred processing the file'}), 500


@socketio.on('start_transcription')
def handle_start_transcription():
    try:
        dg_connection = realtime_transcription.start_realtime_transcription(request.sid)
        socketio.emit('transcription_started', room=request.sid)
        logger.info(f'Started real-time transcription for session: {request.sid}')
    except Exception as e:
        logger.error(f'Error starting transcription: {str(e)}')
        socketio.emit('transcription_error', {'error': 'Failed to start transcription'}, room=request.sid)


@socketio.on('audio_stream')
def handle_audio_stream(audio_chunk):
    try:
        # Save audio chunk
        chunk_path = audio_storage.save_audio(audio_chunk)
        # Send audio chunk to Deepgram
        dg_connection.send(audio_chunk)
        logger.debug(f'Processed audio chunk: {chunk_path}')
    except Exception as e:
        logger.error(f'Error processing audio stream: {str(e)}')


@socketio.on('stop_transcription')
def handle_stop_transcription():
    try:
        realtime_transcription.stop_realtime_transcription(dg_connection)
        socketio.emit('transcription_stopped', room=request.sid)
        logger.info(f'Stopped real-time transcription for session: {request.sid}')
    except Exception as e:
        logger.error(f'Error stopping transcription: {str(e)}')
        socketio.emit('transcription_error', {'error': 'Failed to stop transcription'}, room=request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)
