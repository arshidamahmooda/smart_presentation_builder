import re
from sklearn.feature_extraction.text import TfidfVectorizer

def summarize_text(text, slide_count):
    # Simple sentence splitting without NLTK
    sentences = re.split(r'(?<=[.!?]) +', text.strip())

    if len(sentences) < slide_count:
        slide_count = max(1, len(sentences))

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)
    sentence_scores = tfidf_matrix.sum(axis=1).A1

    sorted_ids = sentence_scores.argsort()[::-1][:slide_count * 3]
    selected = [sentences[i] for i in sorted_ids]
    grouped = [selected[i:i + 3] for i in range(0, len(selected), 3)]

    bullets = [["• " + s for s in group] for group in grouped[:slide_count]]
    return bullets
