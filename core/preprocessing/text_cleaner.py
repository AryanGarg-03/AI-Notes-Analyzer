import re


def clean_text(text):
    if not text:
        return ""

    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9.,;:!?()\-'/ ]", "", text)

    return text.strip()


def split_into_sentences(text):
    text = clean_text(text)

    sentences = re.split(r"(?<=[.!?])\s+", text)

    return [sentence.strip() for sentence in sentences if sentence.strip()]


def split_into_paragraphs(text, max_words=120):
    text = clean_text(text)
    words = text.split()

    paragraphs = []

    for i in range(0, len(words), max_words):
        paragraph = " ".join(words[i:i + max_words])
        paragraphs.append(paragraph)

    return paragraphs