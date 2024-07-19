import librosa
import numpy as np

def analyze_audio(audio_file):
    # Load the audio file
    y, sr = librosa.load(audio_file)

    # Extract features
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # Pitch and pitch variability
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_mean = np.mean(pitches[pitches > 0]) if np.any(pitches > 0) else 0
    pitch_std = np.std(pitches[pitches > 0]) if np.any(pitches > 0) else 0

    # Energy and energy variability
    rms = librosa.feature.rms(y=y)[0]
    energy_mean = np.mean(rms)
    energy_std = np.std(rms)

    # Speech rate (syllables per second)
    syllables = count_syllables(y, sr)
    duration = librosa.get_duration(y=y, sr=sr)
    speech_rate = syllables / duration if duration > 0 else 0

    # Pauses
    pauses = detect_pauses(y, sr)

    # Voice quality (Harmonics-to-Noise Ratio)
    hnr = librosa.feature.spectral_flatness(y=y)[0]
    hnr_mean = np.mean(hnr)

    # Formants (simplified estimation)
    formants = estimate_formants(y, sr)

    return {
        "tempo": tempo,
        "spectral_centroid": np.mean(spectral_centroids),
        "spectral_rolloff": np.mean(spectral_rolloff),
        "mfccs": np.mean(mfccs, axis=1).tolist(),
        "pitch_mean": pitch_mean,
        "pitch_variability": pitch_std,
        "energy_mean": energy_mean,
        "energy_variability": energy_std,
        "speech_rate": speech_rate,
        "pause_count": len(pauses),
        "pause_duration_mean": np.mean(pauses) if pauses else 0,
        "voice_quality_hnr": hnr_mean,
        "formants": formants
    }

def count_syllables(y, sr):
    # This is a simple estimation. For more accurate results, consider using a dedicated syllable counter.
    energy = librosa.feature.rms(y=y)[0]
    peaks = librosa.util.peak_pick(energy, pre_max=3, post_max=3, pre_avg=3, post_avg=3, delta=0.5, wait=10)
    return len(peaks)

def detect_pauses(y, sr, threshold_db=-30, min_pause_duration=0.5):
    # Convert to dB
    y_db = librosa.amplitude_to_db(np.abs(y), ref=np.max)

    # Find pauses
    is_pause = y_db < threshold_db
    pause_samples = np.where(is_pause)[0]

    # Group consecutive pause samples
    pause_groups = np.split(pause_samples, np.where(np.diff(pause_samples) != 1)[0] + 1)

    # Convert to seconds and filter by minimum duration
    pauses = [
        (len(group) / sr) for group in pause_groups
        if (len(group) / sr) >= min_pause_duration
    ]

    return pauses

def estimate_formants(y, sr, n_formants=4):
    # This is a simplified method. For more accurate results, consider using specialized libraries.
    n_fft = 2048
    S = librosa.stft(y, n_fft=n_fft)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

    magnitudes = np.abs(S)
    formants = []

    for i in range(n_formants):
        peak_freq = freqs[np.argmax(magnitudes[:, i])]
        formants.append(peak_freq)

    return formants