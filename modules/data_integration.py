import numpy as np
import logging

logger = logging.getLogger('data_integration_logger')
logging.basicConfig(level=logging.INFO)

def numpy_to_python(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: numpy_to_python(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [numpy_to_python(i) for i in obj]
    else:
        return obj

def integrate_data(audio_features, text_features):
    logger.info("Starting data integration")
    try:
        integrated_data = {
            "audio_features": {
                "tempo": audio_features["tempo"],
                "spectral_centroid": audio_features["spectral_centroid"],
                "spectral_rolloff": audio_features["spectral_rolloff"],
                "mfccs": audio_features["mfccs"],
                "pitch_mean": audio_features["pitch_mean"],
                "pitch_variability": audio_features["pitch_variability"],
                "energy_mean": audio_features["energy_mean"],
                "energy_variability": audio_features["energy_variability"],
                "speech_rate": audio_features["speech_rate"],
                "pause_count": audio_features["pause_count"],
                "pause_duration_mean": audio_features["pause_duration_mean"],
                "voice_quality_hnr": audio_features["voice_quality_hnr"],
                "formants": audio_features["formants"],
                "chroma": audio_features["chroma"]
            },
            "text_features": {
                "sentiment": text_features["sentiment"],
                "word_count": text_features["word_count"],
                "unique_words": text_features["unique_words"]
            },
            "top_words": text_features["top_words"]
        }

        logger.info("Completed data integration")
        return numpy_to_python(integrated_data)
    except Exception as e:
        logger.error(f"Error in data integration: {str(e)}")
        raise
