import numpy as np

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

def integrate_data(audio_analysis, text_analysis):
    integrated_data = {
        "audio_features": {
            "tempo": audio_analysis["tempo"],
            "spectral_centroid": audio_analysis["spectral_centroid"],
            "spectral_rolloff": audio_analysis["spectral_rolloff"]
        },
        "text_features": {
            "sentiment": text_analysis["sentiment"],
            "word_count": text_analysis["word_count"],
            "unique_words": text_analysis["unique_words"]
        },
        "top_words": text_analysis["top_words"],
        "mfccs": audio_analysis["mfccs"]
    }

    return numpy_to_python(integrated_data)