from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import difflib

# Load the SBERT model (for contextual similarity)
model = SentenceTransformer('all-MiniLM-L6-v2')

def check_word_similarity(text1, text2):
    """Checks word-to-word similarity using TF-IDF + Cosine Similarity."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    return similarity[0][0]

def check_semantic_similarity(text1, text2):
    """Computes semantic similarity using SBERT embeddings + Cosine Similarity."""
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)

    similarity = util.pytorch_cos_sim(embedding1, embedding2)
    return similarity.item()

def find_exact_matches(text1, text2):
    """Finds exact word matches between two texts."""
    words1 = set(text1.split())
    words2 = set(text2.split())
    
    common_words = words1.intersection(words2)
    return list(common_words)

def find_similar_sentences(text1, text2, threshold=0.75):
    """Finds paraphrased sentences using SBERT."""
    sentences1 = text1.split(". ")
    sentences2 = text2.split(". ")

    similar_sentences = []
    for sent1 in sentences1:
        for sent2 in sentences2:
            sim_score = check_semantic_similarity(sent1, sent2)
            if sim_score > threshold:
                similar_sentences.append((sent1, sent2, sim_score))

    return similar_sentences

from similarity import check_word_similarity

text1 = "Hello world"
text2 = "Goodbye world"

similarity_score = check_word_similarity(text1, text2)
print(f"Similarity Score: {similarity_score:.4f}")  
