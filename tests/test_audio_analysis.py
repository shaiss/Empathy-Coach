import pytest
from module.audio_analysis import analyze_audio

def test_analyze_audio():
    # Assuming you have a test audio file in the test_data folder
    result = analyze_audio('test_data/sample_audio.wav')

    assert 'tempo' in result
    assert 'spectral_centroid' in result
    assert 'spectral_rolloff' in result
    assert 'mfccs' in result

    assert isinstance(result['tempo'], float)
    assert isinstance(result['spectral_centroid'], float)
    assert isinstance(result['spectral_rolloff'], float)
    assert isinstance(result['mfccs'], list)

def test_analyze_audio_with_invalid_file():
    with pytest.raises(Exception):
        analyze_audio('non_existent_file.wav')