import re
from pypdf import PdfReader
from ebooklib import epub
from bs4 import BeautifulSoup

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def parse_pdf(path):
    reader = PdfReader(path)
    text = "".join([page.extract_text() or "" for page in reader.pages])
    return clean_text(text)

def parse_epub(path):
    book = epub.read_epub(path)
    text = ""
    for item in book.get_items():
        if item.get_type() == epub.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), "html.parser")
            text += soup.get_text() + "\n"
    return clean_text(text)

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
