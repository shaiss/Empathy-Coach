import pytest
from modules import text_analysis

def test_analyze_text():
    sample_text = "This is a very happy and positive test sentence. It contains several different words and expressions. Testing the text analysis module should yield interesting results."

    result = text_analysis.analyze_text(sample_text)

    # Basic structure checks
    assert isinstance(result, dict)
    assert 'sentiment' in result
    assert 'word_count' in result
    assert 'unique_words' in result
    assert 'top_words' in result
    assert 'emotion_analysis' in result
    assert 'readability_scores' in result
    assert 'sentence_analysis' in result
    assert 'named_entities' in result
    assert 'lexical_diversity' in result

    # Sentiment analysis checks
    assert isinstance(result['sentiment'], dict)
    assert 'pos' in result['sentiment']
    assert 'neg' in result['sentiment']
    assert 'neu' in result['sentiment']
    assert 'compound' in result['sentiment']

    # Word count checks
    assert isinstance(result['word_count'], int)
    assert result['word_count'] == 25  # Update this value based on the actual word count of sample_text

    # Unique words check
    assert isinstance(result['unique_words'], int)
    assert result['unique_words'] > 0

    # Top words check
    assert isinstance(result['top_words'], dict)
    assert len(result['top_words']) > 0

    # Emotion analysis checks
    assert isinstance(result['emotion_analysis'], dict)
    assert 'very_positive' in result['emotion_analysis']
    assert 'positive' in result['emotion_analysis']
    assert 'neutral' in result['emotion_analysis']
    assert 'negative' in result['emotion_analysis']
    assert 'very_negative' in result['emotion_analysis']

    # Readability scores checks
    assert isinstance(result['readability_scores'], dict)
    assert 'flesch_reading_ease' in result['readability_scores']
    assert 'flesch_kincaid_grade' in result['readability_scores']
    assert 'gunning_fog' in result['readability_scores']

    # Sentence analysis checks
    assert isinstance(result['sentence_analysis'], dict)
    assert 'sentence_count' in result['sentence_analysis']
    assert 'avg_sentence_length' in result['sentence_analysis']
    assert 'complex_sentence_ratio' in result['sentence_analysis']

    # Named entities checks
    assert isinstance(result['named_entities'], dict)
    assert 'named_entity_count' in result['named_entities']
    assert 'entity_types' in result['named_entities']

    # Lexical diversity check
    assert isinstance(result['lexical_diversity'], float)
    assert 0 <= result['lexical_diversity'] <= 1

    # Validate some specific checks
    assert result['sentiment']['pos'] > result['sentiment']['neg']
    assert isinstance(result['readability_scores']['flesch_reading_ease'], float)
    assert isinstance(result['readability_scores']['flesch_kincaid_grade'], float)
    assert isinstance(result['readability_scores']['gunning_fog'], float)
    assert isinstance(result['sentence_analysis']['sentence_count'], int)
    assert isinstance(result['sentence_analysis']['avg_sentence_length'], float)
    assert isinstance(result['sentence_analysis']['complex_sentence_ratio'], float)
    assert isinstance(result['named_entities']['named_entity_count'], int)
    assert isinstance(result['named_entities']['entity_types'], dict)

if __name__ == '__main__':
    pytest.main()
