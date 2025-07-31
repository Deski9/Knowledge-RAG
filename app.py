import streamlit as st
import os
import tempfile
import faiss
import numpy as np
from utils.text_utils import parse_pdf, parse_epub, chunk_text
from utils.embed_utils import embed_chunks, build_faiss_index, load_index, load_mapping
from utils.query_utils import build_prompt, query_ollama
from sentence_transformers import CrossEncoder

INDEX_PATH = "faiss_index.bin"
MAPPING_PATH = "mapping.json"
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")

st.set_page_config(page_title="Knowledge-RAG", page_icon="📚", layout="wide")
st.title("📚 Knowledge-RAG")

mode = st.radio("Choose Mode:", ["Use Pre-Indexed Books", "Upload New Document"])
query = st.text_input("Enter your question:")
k = st.slider("Number of FAISS candidates", min_value=5, max_value=20, value=10)
rerank_top = st.slider("Number of top reranked results", min_value=1, max_value=5, value=3)

retrieved = []

if mode == "Use Pre-Indexed Books" and query:
    try:
        from utils.query_utils import retrieve_chunks
        retrieved = retrieve_chunks(query, k=k, rerank_top=rerank_top,
                                    index_path=INDEX_PATH, mapping_path=MAPPING_PATH)
    except Exception:
        st.error("No FAISS index found. Please run embed.py first.")

if mode == "Upload New Document":
    uploaded_file = st.file_uploader("Upload a PDF or EPUB", type=["pdf", "epub"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        if uploaded_file.name.lower().endswith(".pdf"):
            text = parse_pdf(tmp_path)
        elif uploaded_file.name.lower().endswith(".epub"):
            text = parse_epub(tmp_path)
        else:
            st.error("Unsupported file type")
            st.stop()

        os.remove(tmp_path)

        chunks = chunk_text(text)
        embeddings = embed_chunks(chunks)
        index = build_faiss_index(embeddings)
        mapping = {i: {"book": uploaded_file.name, "chunk": chunk} for i, chunk in enumerate(chunks)}

        if query:
            query_embedding = embed_chunks([query])
            distances, indices = index.search(query_embedding, k)
            candidates = [(mapping[idx]["book"], mapping[idx]["chunk"]) for idx in indices[0]]

            pairs = [(query, chunk) for (_, chunk) in candidates]
            scores = reranker.predict(pairs)
            retrieved = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)[:rerank_top]

if query and retrieved:
    prompt = build_prompt(query, retrieved)
    try:
        answer = query_ollama(prompt)
    except Exception:
        answer = "⚠️ Ollama not running. Showing retrieved chunks only."

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Sources")
    for rank, ((book, chunk), score) in enumerate(retrieved):
        with st.expander(f"{rank+1}. {book} (Score: {score:.4f})"):
            st.write(chunk[:500])
