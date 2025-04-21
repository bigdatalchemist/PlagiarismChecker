import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="plagiarism_checker"
    )

def insert_document(title, content):
    """Insert document text into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO documents (title, content) VALUES (%s, %s)", (title, content))
    conn.commit()
    conn.close()

def fetch_documents():
    """Retrieve all stored documents."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM documents")
    documents = cursor.fetchall()
    conn.close()
    return documents
