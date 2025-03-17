import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def get_stopwords():
    """Fetch stopwords, downloading them if necessary."""
    try:
        return set(stopwords.words('english'))
    except LookupError:
        nltk.download('stopwords')
        return set(stopwords.words('english'))

STOPWORDS = get_stopwords()

def preprocess_text(text):
    """
    Cleans and tokenizes text.
    
    Steps:
    1. Convert to lowercase
    2. Remove punctuation & special characters
    3. Tokenize into words
    4. Remove stopwords
    5. Return cleaned text as a string
    """
    if not text or not isinstance(text, str):
        raise ValueError("Error: Input text must be a non-empty string.")

    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W+', ' ', text)  # Remove punctuation
    words = word_tokenize(text)  # Tokenize text
    words = [word for word in words if word not in STOPWORDS]  # Remove stopwords

    return " ".join(words)  # Return cleaned text as a string
