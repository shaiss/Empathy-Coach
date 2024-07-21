import pytest
from modules.audio_analysis import analyze_audio
import numpy as np
import os
import scipy.io.wavfile as wav

@pytest.fixture
def sample_audio_file(tmp_path):
    ## Create a dummy audio file for testing
    #duration = 5  # seconds
    #sample_rate = 44100
    #t = np.linspace(0, duration, int(sample_rate * duration), False)
    #data = np.sin(440 * 2 * np.pi * t) + np.sin(880 * 2 * np.pi * t)  # 440 Hz and 880 Hz sine waves
    #file_path = os.path.join(tmp_path, "test_audio.wav")
    #wav.write(file_path, sample_rate, (data * 32767).astype(np.int16))
    #return file_path
    return os.path.join('tests', 'test_data', 'sample_audio.wav')

def test_analyze_audio(sample_audio_file):
    result = analyze_audio(sample_audio_file)

    assert isinstance(result, dict)
    expected_keys = [
        'tempo', 'spectral_centroid', 'spectral_rolloff', 'zero_crossing_rate_mean',
        'mfccs_mean', 'pitch_mean', 'pitch_variability', 'energy_mean', 'energy_variability',
        'speech_rate', 'pause_count', 'pause_duration_mean', 'voice_quality_hnr', 'formants'
    ]
    for key in expected_keys:
        assert key in result, f"Expected key '{key}' not found in result"

    for key, value in result.items():
        if key != 'mfccs_mean' and key != 'formants':
            assert isinstance(value, (float, int)), f"Expected {key} to be float or int, but got {type(value)}"
        if isinstance(value, float):
            assert np.isfinite(value), f"Expected {key} to be finite, but got {value}"

    assert isinstance(result['mfccs_mean'], list)
    assert len(result['mfccs_mean']) == 13  # We specified 13 MFCCs
    assert isinstance(result['formants'], list)

def test_analyze_audio_with_invalid_file(tmp_path):
    invalid_file = os.path.join(tmp_path, "invalid.wav")
    with open(invalid_file, 'w') as f:
        f.write("This is not a valid audio file")

    with pytest.raises(Exception):
        analyze_audio(invalid_file)
