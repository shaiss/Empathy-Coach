import nltk
import spacy
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from textstat import textstat
from modules.logger import setup_logger

# Setup logging
logger = setup_logger('text_analysis_logger', 'logs/text_analysis.log')

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('vader_lexicon', quiet=True)

nlp = spacy.load('en_core_web_sm')

def analyze_text(transcript):
    try:
        logger.info('Starting text analysis')

        # Tokenize and remove stopwords
        stop_words = set(stopwords.words('english'))
        words = [w.lower() for w in word_tokenize(transcript) if w.isalnum()]
        filtered_words = [w for w in words if w not in stop_words]

        # Perform sentiment analysis
        sia = SentimentIntensityAnalyzer()
        sentiment_scores = sia.polarity_scores(transcript)

        # Count word frequency
        word_freq = FreqDist(filtered_words)

        # Readability and complexity metrics
        readability_scores = {
            "flesch_reading_ease": textstat.flesch_reading_ease(transcript),
            "flesch_kincaid_grade": textstat.flesch_kincaid_grade(transcript),
            "gunning_fog": textstat.gunning_fog(transcript)
        }

        # Sentence structure analysis
        sentence_analysis = analyze_sentence_structure(transcript)

        # Named Entity Recognition
        ner_analysis = analyze_named_entities(transcript)

        # Lexical diversity
        lexical_diversity = len(set(filtered_words)) / len(filtered_words) if filtered_words else 0

        # Emotion analysis using VADER
        emotion_analysis = analyze_emotions(transcript)

        features = {
            "sentiment": sentiment_scores,
            "word_count": len(words),
            "unique_words": len(set(filtered_words)),
            "top_words": dict(word_freq.most_common(10)),
            "emotion_analysis": emotion_analysis,
            "readability_scores": readability_scores,
            "sentence_analysis": sentence_analysis,
            "named_entities": ner_analysis,
            "lexical_diversity": lexical_diversity
        }

        logger.info('Completed text analysis')
        return features
    except Exception as e:
        logger.error(f'Error during text analysis: {str(e)}')
        raise

def analyze_emotions(text):
    sia = SentimentIntensityAnalyzer()
    sentences = sent_tokenize(text)
    emotion_counts = {
        "very_positive": 0,
        "positive": 0,
        "neutral": 0,
        "negative": 0,
        "very_negative": 0
    }

    for sentence in sentences:
        scores = sia.polarity_scores(sentence)
        compound = scores['compound']
        if compound >= 0.5:
            emotion_counts["very_positive"] += 1
        elif 0.1 <= compound < 0.5:
            emotion_counts["positive"] += 1
        elif -0.1 < compound < 0.1:
            emotion_counts["neutral"] += 1
        elif -0.5 < compound <= -0.1:
            emotion_counts["negative"] += 1
        else:
            emotion_counts["very_negative"] += 1

    return emotion_counts

def analyze_sentence_structure(text):
    sentences = sent_tokenize(text)
    return {
        "sentence_count": len(sentences),
        "avg_sentence_length": sum(len(word_tokenize(sent)) for sent in sentences) / len(sentences) if sentences else 0,
        "complex_sentence_ratio": sum(1 for sent in sentences if len(word_tokenize(sent)) > 20) / len(sentences) if sentences else 0
    }

def analyze_named_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return {
        "named_entity_count": len(entities),
        "entity_types": {ent_type: entities.count(ent_type) for ent_type in set(ent[1] for ent in entities)}
    }
