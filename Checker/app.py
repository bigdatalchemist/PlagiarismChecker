import streamlit as st
import nltk
import os
from text_processing import preprocess_text
from similarity import (
    check_word_similarity,
    check_semantic_similarity,
    find_exact_matches,
    find_similar_sentences
)
from webscrapper import extract_text_from_url
from utils import extract_text

# Get the absolute path of the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set a persistent NLTK data directory inside the project
NLTK_DIR = os.path.join(BASE_DIR, "nltk_data")
os.makedirs(NLTK_DIR, exist_ok=True)

# Add the directory to NLTK's path
nltk.data.path.append(NLTK_DIR)

# Ensure the necessary NLTK resources are downloaded
nltk.download('punkt', download_dir=NLTK_DIR, quiet=True)
nltk.download('punkt_tab', download_dir=NLTK_DIR, quiet=True)
nltk.download('stopwords', download_dir=NLTK_DIR, quiet=True)

def load_css():
    """Load custom CSS from an external file."""
    css_file = os.path.join(BASE_DIR, "Checker", "styles.css")
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the CSS file
load_css()

st.title("🔍 Plagiarism Checker")

# Select input type
option = st.radio("Choose input type:", ["Enter Text", "Upload File", "Check URL"])

text1 = None
text2 = None

if option == "Enter Text":
    text1 = st.text_area("Enter First Text")
    text2 = st.text_area("Enter Second Text")

elif option == "Upload File":
    uploaded_file1 = st.file_uploader("Upload First Document", type=["txt", "docx", "pdf"])
    uploaded_file2 = st.file_uploader("Upload Second Document", type=["txt", "docx", "pdf"])

    if uploaded_file1 and uploaded_file2:
        text1 = extract_text(uploaded_file1)
        text2 = extract_text(uploaded_file2)

elif option == "Check URL":
    url1 = st.text_input("Enter First URL")
    url2 = st.text_input("Enter Second URL")

    if url1 and url2:
        text1 = extract_text_from_url(url1)
        text2 = extract_text_from_url(url2)

# Process and check similarity
if text1 and text2:
    cleaned_text1 = preprocess_text(text1)
    cleaned_text2 = preprocess_text(text2)

    word_similarity_score = check_word_similarity(cleaned_text1, cleaned_text2)
    semantic_similarity_score = check_semantic_similarity(cleaned_text1, cleaned_text2)

    # Identify plagiarism sections
    exact_matches = find_exact_matches(cleaned_text1, cleaned_text2)
    similar_sentences = find_similar_sentences(cleaned_text1, cleaned_text2)

    st.subheader("📊 Plagiarism Detection Results")
    st.write(f"📝 **Word-Based Similarity Score:** {word_similarity_score:.4f}")
    st.write(f"🤖 **Context-Based Similarity Score:** {semantic_similarity_score:.4f}")

    if semantic_similarity_score > 0.8:
        st.error("⚠️ High contextual similarity detected! The texts may be paraphrased plagiarism.")
    elif word_similarity_score > 0.8:
        st.error("⚠️ High word-level similarity detected! Possible plagiarism.")
    elif semantic_similarity_score > 0.5:
        st.warning("⚠️ Moderate contextual similarity detected.")
    else:
        st.success("✅ The texts appear unique.")

    # Show exact plagiarized words
    if exact_matches:
        st.subheader("🔍 Exact Word Matches")
        st.write(", ".join(exact_matches))

    # Show paraphrased sentences
    if similar_sentences:
        st.subheader("📖 Paraphrased Sentences Detected")
        for sent1, sent2, score in similar_sentences:
            st.write(f"🔹 **Original:** {sent1}")
            st.write(f"🔹 **Similar:** {sent2}")
            st.write(f"📊 **Similarity Score:** {score:.2f}")
            st.write("---")