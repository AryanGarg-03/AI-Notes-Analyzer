from preprocessing.text_cleaner import (
    clean_text,
    split_into_sentences,
    split_into_paragraphs
)
from nlp.keyword_extractor import extract_tfidf_keywords
from nlp.concept_extractor import extract_concepts


def analyze_notes_fast(raw_text):
    cleaned_text = clean_text(raw_text)
    sentences = split_into_sentences(cleaned_text)
    paragraphs = split_into_paragraphs(cleaned_text)

    keywords = extract_tfidf_keywords(cleaned_text, top_n=15)

    analysis = {
        "analysis_mode": "fast_classical_nlp",
        "cleaned_text": cleaned_text,
        "statistics": {
            "total_characters": len(cleaned_text),
            "total_words": len(cleaned_text.split()),
            "total_sentences": len(sentences),
            "total_paragraph_chunks": len(paragraphs)
        },
        "keywords": keywords,
        "concepts": []
    }

    return analysis


def analyze_notes_advanced(raw_text):
    cleaned_text = clean_text(raw_text)
    sentences = split_into_sentences(cleaned_text)
    paragraphs = split_into_paragraphs(cleaned_text)

    keywords = extract_tfidf_keywords(cleaned_text, top_n=15)
    concepts = extract_concepts(cleaned_text, top_n=10)

    analysis = {
        "analysis_mode": "advanced_transformer_nlp",
        "cleaned_text": cleaned_text,
        "statistics": {
            "total_characters": len(cleaned_text),
            "total_words": len(cleaned_text.split()),
            "total_sentences": len(sentences),
            "total_paragraph_chunks": len(paragraphs)
        },
        "keywords": keywords,
        "concepts": concepts
    }

    return analysis


def analyze_notes_with_nlp(raw_text, threshold_chars=5000):
    cleaned_text = clean_text(raw_text)

    if len(cleaned_text) < threshold_chars:
        return analyze_notes_fast(raw_text)

    return analyze_notes_advanced(raw_text)