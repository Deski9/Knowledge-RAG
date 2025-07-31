from utils.text_utils import chunk_text
from utils.embed_utils import embed_chunks, build_faiss_index, save_index, save_mapping
import os
import json

PROCESSED_DIR = "processed"
INDEX_PATH = "faiss_index.bin"
MAPPING_PATH = "mapping.json"

def build_index():
    documents = []
    mapping = {}

    for file in os.listdir(PROCESSED_DIR):
        if not file.endswith(".txt"):
            continue
        path = os.path.join(PROCESSED_DIR, file)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        for idx, chunk in enumerate(chunks):
            documents.append(chunk)
            mapping[len(mapping)] = {"book": file, "chunk": chunk}

    embeddings = embed_chunks(documents)
    index = build_faiss_index(embeddings)

    save_index(index, INDEX_PATH)
    save_mapping(mapping, MAPPING_PATH)

    print(f"Indexed {len(documents)} chunks from {len(os.listdir(PROCESSED_DIR))} books.")

if __name__ == "__main__":
    build_index()
