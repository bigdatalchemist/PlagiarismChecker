import os
import docx
import fitz

def extract_text(file):
    """Extract text from TXT, DOCX, or PDF files."""
    if file.name.endswith(".txt"):
        return file.getvalue().decode("utf-8")

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    elif file.name.endswith(".pdf"):
        pdf_text = []
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                pdf_text.append(page.get_text())
        return "\n".join(pdf_text)

    return ""