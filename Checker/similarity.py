from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import difflib
import torch
import os

# Load the SBERT model from a local folder (avoids Streamlit Cloud issues)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "my_model")

model = SentenceTransformer(MODEL_DIR)

def check_word_similarity(text1, text2):
    """Checks word-to-word similarity using TF-IDF + Cosine Similarity."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    return similarity[0][0]

def check_semantic_similarity(text1, text2):
    """Checks semantic similarity using SBERT + Cosine Similarity."""
    embeddings = model.encode([text1, text2], convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    return similarity.item()

def find_exact_matches(text1, text2):
    """Finds exact matching words between two texts."""
    words1 = set(text1.split())
    words2 = set(text2.split())
    matches = words1.intersection(words2)
    return list(matches)

def find_similar_sentences(text1, text2, threshold=0.7):
    """Finds paraphrased sentences by comparing sentence embeddings."""
    sentences1 = text1.split(". ")
    sentences2 = text2.split(". ")
    
    similar_pairs = []
    
    for sent1 in sentences1:
        for sent2 in sentences2:
            score = check_semantic_similarity(sent1, sent2)
            if score > threshold:
                similar_pairs.append((sent1, sent2, score))
    
    return similar_pairs
