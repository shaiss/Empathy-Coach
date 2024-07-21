from flask import jsonify, request, render_template
from flask_socketio import SocketIO
from modules.text_analysis import analyze_text
from modules import realtime_transcription, file_transcription, feedback_generation, database
import logging

logger = logging.getLogger(__name__)

# List of allowed audio file extensions
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a', 'mp4'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_routes(app, socketio, db):
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

        if file and allowed_file(file.filename):
            try:
                # Send file directly to Deepgram
                transcript = file_transcription.transcribe_file(file)
                logger.info("Transcription completed")

                if not transcript:
                    logger.error("Received empty transcript")
                    return jsonify({'error': 'Failed to transcribe the file'}), 500

                # Perform text analysis
                text_features = analyze_text(transcript)

                # Generate feedback
                feedback = feedback_generation.generate_feedback(text_features)

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
        else:
            return jsonify({'error': 'File type not allowed'}), 400

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
            # Send audio chunk to Deepgram
            dg_connection.send(audio_chunk)
            logger.debug('Processed audio chunk')
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