from nlp.keyword_extractor import extract_tfidf_keywords
from nlp.embedding_engine import (
    create_paragraph_embeddings,
    find_similar_paragraphs_from_embeddings
)


def extract_concepts(text, top_n=10):
    keywords = extract_tfidf_keywords(text, top_n=top_n)

    embedding_data = create_paragraph_embeddings(text)
    paragraphs = embedding_data["paragraphs"]
    embeddings = embedding_data["embeddings"]

    concepts = []

    for keyword_data in keywords:
        keyword = keyword_data["keyword"]
        score = keyword_data["score"]

        related_paragraphs = find_similar_paragraphs_from_embeddings(
            query=keyword,
            paragraphs=paragraphs,
            embeddings=embeddings,
            top_n=1
        )

        concepts.append({
            "concept": keyword,
            "importance_score": score,
            "related_paragraphs": related_paragraphs
        })

    return concepts