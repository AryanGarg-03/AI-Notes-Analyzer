from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing.text_cleaner import split_into_paragraphs


MODEL_NAME = "all-MiniLM-L6-v2"

_model = None


def get_embedding_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def create_paragraph_embeddings(text):
    paragraphs = split_into_paragraphs(text)

    if not paragraphs:
        return {
            "paragraphs": [],
            "embeddings": []
        }

    model = get_embedding_model()
    embeddings = model.encode(paragraphs)

    return {
        "paragraphs": paragraphs,
        "embeddings": embeddings
    }


def find_similar_paragraphs_from_embeddings(query, paragraphs, embeddings, top_n=3):
    if len(paragraphs) == 0:
        return []

    model = get_embedding_model()
    query_embedding = model.encode([query])

    similarity_scores = cosine_similarity(query_embedding, embeddings)[0]

    results = []

    for index, score in enumerate(similarity_scores):
        results.append({
            "paragraph": paragraphs[index],
            "similarity_score": round(float(score), 4)
        })

    results = sorted(
        results,
        key=lambda item: item["similarity_score"],
        reverse=True
    )

    return results[:top_n]


def find_similar_paragraphs(query, text, top_n=3):
    embedding_data = create_paragraph_embeddings(text)

    return find_similar_paragraphs_from_embeddings(
        query=query,
        paragraphs=embedding_data["paragraphs"],
        embeddings=embedding_data["embeddings"],
        top_n=top_n
    )