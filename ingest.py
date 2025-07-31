from utils.text_utils import parse_pdf, parse_epub, clean_text
import os
import sys

DATA_DIR = "data"
PROCESSED_DIR = "processed"

def ingest_books(force=False):
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    texts = {}

    for file in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, file)
        cached_path = os.path.join(PROCESSED_DIR, file.replace(".pdf", ".txt").replace(".epub", ".txt"))

        if not force and os.path.exists(cached_path):
            with open(cached_path, "r", encoding="utf-8") as f:
                texts[file] = f.read()
            print(f"[CACHE] Loaded {file}")
            continue

        if file.lower().endswith(".pdf"):
            content = parse_pdf(path)
        elif file.lower().endswith(".epub"):
            content = parse_epub(path)
        else:
            print(f"[SKIP] Unsupported file: {file}")
            continue

        texts[file] = content
        with open(cached_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[NEW] Ingested {file}")

    return texts

if __name__ == "__main__":
    force = len(sys.argv) > 1 and sys.argv[1] == "force"
    ingest_books(force=force)
