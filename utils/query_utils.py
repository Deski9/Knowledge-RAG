import json
import requests
from sentence_transformers import SentenceTransformer, CrossEncoder
from utils.embed_utils import load_index, load_mapping

# Models
bi_encoder = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")

# Ollama API
OLLAMA_API = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

def retrieve_chunks(query, k=10, rerank_top=3, index_path="faiss_index.bin", mapping_path="mapping.json"):
    """
    Retrieve top-k chunks from FAISS and rerank them with CrossEncoder.
    """
    index = load_index(index_path)
    mapping = load_mapping(mapping_path)

    query_embedding = bi_encoder.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, k)

    candidates = [(mapping[str(idx)]["book"], mapping[str(idx)]["chunk"]) for idx in indices[0]]

    pairs = [(query, chunk) for (_, chunk) in candidates]
    scores = reranker.predict(pairs)

    reranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return reranked[:rerank_top]

def build_prompt(query, retrieved):
    """
    Build a prompt for Ollama using retrieved context.
    """
    context = "\n\n".join([f"From {book}: {chunk[:500]}" for (book, chunk), _ in retrieved])
    return f"""Answer the following question using the provided context. 
If the context is insufficient, say you don't know.

Context:
{context}

Question: {query}

Answer:"""

def query_ollama(prompt, model=OLLAMA_MODEL):
    """
    Send prompt to Ollama API and return the generated answer.
    """
    data = {"model": model, "prompt": prompt}
    response = requests.post(OLLAMA_API, json=data, stream=True)
    answer = ""
    for line in response.iter_lines():
        if line:
            part = json.loads(line.decode("utf-8"))
            if "response" in part:
                answer += part["response"]
    return answer.strip()
