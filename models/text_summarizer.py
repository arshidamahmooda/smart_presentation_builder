from sklearn.feature_extraction.text import TfidfVectorizer
from io import BytesIO
import nltk
nltk.download('punkt')

def summarize_text(text, slide_count):
    sentences = nltk.sent_tokenize(text)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)
    sentence_scores = tfidf_matrix.sum(axis=1).A1

    sorted_ids = sentence_scores.argsort()[::-1][:slide_count * 3]

    selected = [sentences[i] for i in sorted_ids]
    grouped = [selected[i:i+3] for i in range(0, len(selected), 3)]
    
    bullets = [["• " + s for s in group] for group in grouped[:slide_count]]
    return bullets
