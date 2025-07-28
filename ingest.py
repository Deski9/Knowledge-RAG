import os
import pypdf
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

DATA_DIR = "data"
CACHE_DIR = "processed"
os.makedirs(CACHE_DIR, exist_ok=True)

def load_pdf(path):
    text = ""
    with open(path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return clean_text(text)

def load_epub(path):
    text = ""
    book = epub.read_epub(path)
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), "html.parser")
            text += soup.get_text() + "\n"
    return clean_text(text)

def get_cached_path(filename):
    base = os.path.splitext(filename)[0]
    return os.path.join(CACHE_DIR, f"{base}.txt")

def ingest_books(force=False):
    texts = {}
    for file in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, file)
        cached_path = get_cached_path(file)

        if not force and os.path.exists(cached_path):
            with open(cached_path, "r", encoding="utf-8") as f:
                texts[file] = clean_text(f.read())
            print(f"[CACHE] Loaded {file}")
            continue

        # Otherwise parse and save
        if file.lower().endswith(".pdf"):
            content = load_pdf(path)
        elif file.lower().endswith(".epub"):
            content = load_epub(path)
        else:
            print(f"[SKIP] Unsupported file: {file}")
            continue

        content = clean_text(content)
        texts[file] = content
        with open(cached_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[NEW] Ingested and cached {file}")

    return texts


import re

def clean_text(text):
    # Replace tabs, newlines, and multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


if __name__ == "__main__":
    corpus = ingest_books(force=True)
    for book, text in corpus.items():
        print(f"{book}: {len(text.split())} words")
