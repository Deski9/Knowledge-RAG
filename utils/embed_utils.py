import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model globally so we don’t reload every call
bi_encoder = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    """
    Create embeddings for a list of text chunks.
    Returns a numpy array of embeddings.
    """
    return bi_encoder.encode(chunks, convert_to_numpy=True, show_progress_bar=True)

def build_faiss_index(embeddings):
    """
    Build a FAISS index from embeddings.
    """
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def save_index(index, path):
    """
    Save a FAISS index to disk.
    """
    faiss.write_index(index, path)

def load_index(path):
    """
    Load a FAISS index from disk.
    """
    return faiss.read_index(path)

def save_mapping(mapping, path):
    """
    Save mapping (id -> book/chunk) as JSON.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(mapping, f)

def load_mapping(path):
    """
    Load mapping from JSON file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
