import os
import faiss
import json
import requests
from sentence_transformers import SentenceTransformer, CrossEncoder

# Paths
INDEX_PATH = "faiss_index.bin"
MAPPING_PATH = "mapping.json"

# Load models
bi_encoder = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')

# Ollama API endpoint
OLLAMA_API = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

def retrieve_chunks(query, k=10, rerank_top=3):
    """Retrieve and optionally rerank chunks from FAISS"""
    index = faiss.read_index(INDEX_PATH)

    with open(MAPPING_PATH, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    query_embedding = bi_encoder.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, k)

    candidates = [(mapping[str(idx)]["book"], mapping[str(idx)]["chunk"]) for idx in indices[0]]

    pairs = [(query, chunk) for (_, chunk) in candidates]
    scores = reranker.predict(pairs)
    reranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)

    return reranked[:rerank_top]

def build_prompt(query, retrieved):
    context = "\n\n".join([f"From {book}: {chunk[:500]}" for (book, chunk), _ in retrieved])
    return f"""Answer the following question using the provided context. 
If the context is insufficient, say you don't know.

Context:
{context}

Question: {query}

Answer:"""

def query_ollama(prompt):
    data = {"model": OLLAMA_MODEL, "prompt": prompt}
    response = requests.post(OLLAMA_API, json=data, stream=True)
    answer = ""
    for line in response.iter_lines():
        if line:
            part = json.loads(line.decode("utf-8"))
            if "response" in part:
                answer += part["response"]
    return answer.strip()

if __name__ == "__main__":
    print("📚 Knowledge-RAG Interactive Mode")
    print("Type your question, or type 'exit' to quit.\n")

    while True:
        user_query = input("Your question: ")
        if user_query.strip().lower() == "exit":
            print("Goodbye! 👋")
            break

        retrieved = retrieve_chunks(user_query, k=10, rerank_top=3)
        prompt = build_prompt(user_query, retrieved)

        print("\n--- Thinking... ---\n")
        try:
            answer = query_ollama(prompt)
        except Exception as e:
            answer = "⚠️ Ollama is not running or failed. Showing top retrieved chunks only."

        print("\n--- Final Answer ---\n")
        print(answer)
        print("\n--- Sources ---")
        for rank, ((book, chunk), score) in enumerate(retrieved):
            print(f"{rank+1}. {book} (Score: {score:.4f})")
            print(f"Preview: {chunk[:200]}...")
            print("-" * 60)
