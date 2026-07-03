from sklearn.feature_extraction.text import TfidfVectorizer
from preprocessing.text_cleaner import split_into_paragraphs
def extract_tfidf_keywords(text, top_n=15):
    paragraphs = split_into_paragraphs(text)

    if not paragraphs:
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=500,
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(paragraphs)
    feature_names = vectorizer.get_feature_names_out()

    scores = tfidf_matrix.sum(axis=0).A1

    keyword_scores = []

    for index, score in enumerate(scores):
        keyword_scores.append({
            "keyword": feature_names[index],
            "score": round(float(score), 4)
        })

    keyword_scores = sorted(
        keyword_scores,
        key=lambda item: item["score"],
        reverse=True
    )

    return keyword_scores[:top_n]