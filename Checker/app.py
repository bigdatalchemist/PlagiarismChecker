import streamlit as st
import nltk
import os

from text_processing import preprocess_text
from similarity import check_word_similarity
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

st.title("🔍 Plagiarism Checker")

# Select input type
option = st.radio("Choose input type:", ["Enter Text", "Upload File", "Check URL"])

text1 = None
text2 = None

if option == "Enter Text":
    text1 = st.text_area("Enter First Text")
    text2 = st.text_area("Enter Second Text")

elif option == "Upload File":
    uploaded_file1 = st.file_uploader("Upload First Document", type=["txt", "docx"])
    uploaded_file2 = st.file_uploader("Upload Second Document", type=["txt", "docx"])

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

    similarity_score = check_word_similarity(cleaned_text1, cleaned_text2)

    st.subheader("Plagiarism Detection Results")
    st.write(f"🔍 **Similarity Score:** {similarity_score:.4f}")

    if similarity_score > 0.8:
        st.error("⚠️ High similarity detected! Possible plagiarism.")
    elif similarity_score > 0.5:
        st.warning("⚠️ Moderate similarity detected.")
    else:
        st.success("✅ Low similarity detected. Texts are mostly unique.")
