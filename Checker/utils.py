import os
import docx

def extract_text_from_docx(file_path):
    """Extracts text from a DOCX file."""
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file):
    """Extracts text from different file formats."""
    _, ext = os.path.splitext(file.name)
    if ext == ".txt":
        return file.read().decode("utf-8")
    elif ext == ".docx":
        return extract_text_from_docx(file)
    else:
        return None
