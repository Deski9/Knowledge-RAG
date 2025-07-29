import os
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder

PROCESSED_DIR = "processed"
INDEX_PATH = "faiss_index.bin"
MAPPING_PATH = "mapping.json"

model = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')
def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into overlapping chunks.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

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

 
    embeddings = model.encode(documents, convert_to_numpy=True, show_progress_bar=True)


    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    with open(MAPPING_PATH, "w", encoding="utf-8") as f:
        json.dump(mapping, f)

    print(f"Indexed {len(documents)} chunks from {len(os.listdir(PROCESSED_DIR))} books.")

def test_query(query, k=10, rerank_top=3):
    # Load FAISS index
    index = faiss.read_index(INDEX_PATH)

    # Load mapping
    with open(MAPPING_PATH, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    # Embed the query
    query_embedding = model.encode([query], convert_to_numpy=True)

    # Search FAISS for candidate chunks
    distances, indices = index.search(query_embedding, k)

    # Collect candidate docs with metadata
    candidates = []
    for idx in indices[0]:
        match = mapping[str(idx)]
        candidates.append((match["book"], match["chunk"]))

    # Re-rank using CrossEncoder
    pairs = [(query, chunk) for (_, chunk) in candidates] 
    scores = reranker.predict(pairs)

    # Sort by reranker scores
    reranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)

    print(f"\nQuery: {query}\n")
    for rank, ((book, chunk), score) in enumerate(reranked[:rerank_top]):
        print(f"Result {rank+1}:")
        print(f"Book: {book}")
        print(f"Score: {score:.4f}")
        print(f"Chunk: {chunk[:300]}...") 
        print("-" * 80)



if __name__ == "__main__":
    if not os.path.exists(INDEX_PATH):
        build_index()
    test_query("who is judge holden?")