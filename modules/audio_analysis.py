import librosa
import numpy as np
import logging

logger = logging.getLogger('audio_analysis_logger')
logging.basicConfig(level=logging.INFO)

def analyze_audio(file_path):
    logger.info(f'Starting audio analysis for file: {file_path}')

    try:
        # Load the audio file
        y, sr = librosa.load(file_path)

        # Extract features
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y)[0]
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)

        # Pitch analysis
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_mean = np.mean(pitches[pitches > 0])
        pitch_variability = np.std(pitches[pitches > 0])

        # Energy analysis
        energy = librosa.feature.rms(y=y)[0]
        energy_mean = np.mean(energy)
        energy_variability = np.std(energy)

        # Speech rate (rough estimate)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        speech_rate = len(librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)) / (len(y) / sr)

        # Pause analysis (rough estimate)
        silence_threshold = 0.1 * np.max(y)
        pauses = librosa.effects.split(y, top_db=silence_threshold)
        pause_count = len(pauses) - 1
        pause_duration_mean = np.mean([pause[0] - pauses[i-1][1] for i, pause in enumerate(pauses[1:], 1)]) / sr if pause_count > 0 else 0

        # Voice quality (Harmonics-to-Noise Ratio, rough estimate)
        voice_quality_hnr = np.mean(librosa.effects.harmonic(y)) / np.mean(librosa.effects.percussive(y))

        # Formants (rough estimate)
        formants = librosa.lpc(y, order=5)[1:]

        # Calculate means for features used in proposed code
        mfccs_mean = np.mean(mfccs, axis=1)
        spectral_centroid_mean = np.mean(spectral_centroids)
        chroma_mean = np.mean(chroma, axis=1)

        features = {
            'tempo': float(tempo) if np.isscalar(tempo) else float(tempo[0]),
            'spectral_centroid': float(spectral_centroid_mean),
            'spectral_rolloff': float(np.mean(spectral_rolloff)),
            'zero_crossing_rate_mean': float(np.mean(zero_crossing_rate)),
            'mfccs': mfccs_mean.tolist(),  # Convert to list for JSON serialization
            'pitch_mean': float(pitch_mean),
            'pitch_variability': float(pitch_variability),
            'energy_mean': float(energy_mean),
            'energy_variability': float(energy_variability),
            'speech_rate': float(speech_rate),
            'pause_count': int(pause_count),
            'pause_duration_mean': float(pause_duration_mean),
            'voice_quality_hnr': float(voice_quality_hnr),
            'formants': [float(f) for f in formants],
            'chroma': chroma_mean.tolist()  # Convert to list for JSON serialization
        }

        logger.info(f'Completed audio analysis for file: {file_path}')
        return features
    except Exception as e:
        logger.error(f'Error during audio analysis: {str(e)}')
        raise
