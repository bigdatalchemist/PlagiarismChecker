from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def check_word_similarity(text1, text2):
    """Checks word-to-word similarity using TF-IDF + Cosine Similarity."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    return similarity[0][0]

from similarity import check_word_similarity

text1 = "Hello world"
text2 = "Goodbye world"

similarity_score = check_word_similarity(text1, text2)
print(f"Similarity Score: {similarity_score:.4f}")  
