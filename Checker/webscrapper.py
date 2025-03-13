import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    """Fetches and extracts readable text from a webpage."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return ""  # This return is inside the function

    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")  # Extract paragraph text
    text = " ".join([para.get_text() for para in paragraphs])

    # If no paragraph text found, get the entire webpage text
    if not text.strip():
        text = soup.get_text()

    print(f"\n🔍 Extracted Text from {url}:\n{text[:500]}...\n")  # Debugging
    return text  # This return is also inside the function

