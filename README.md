# Knowledge-RAG

A prototype Retrieval-Augmented Generation (RAG) system for querying books and documents.  
This project demonstrates ingestion, caching, chunking, embeddings, semantic retrieval, and LLM-based question answering using FAISS, CrossEncoder reranking, and Ollama.  
The codebase is modularized with reusable utility modules for ingestion, embeddings, and querying, and includes a Streamlit UI with document upload.

---

## 🚀 Current Features

- Environment setup with a dedicated Python virtual environment  
- Book ingestion supporting both PDF and EPUB formats  
- Caching system: saves parsed `.txt` files in processed/ so ingestion only runs once per book  
- Text cleaning: normalizes whitespace (removes tabs, multiple spaces, and line breaks)  
- Chunking of ingested text into overlapping sections for semantic embeddings  
- FAISS vector store built from book embeddings for efficient similarity search  
- CrossEncoder reranker for improved relevance ranking  
- Ollama integration for generating natural language answers  
- Interactive CLI loop: ask multiple questions until you type `exit`  
- Streamlit interface with two modes:
  - Use Pre-Indexed Books (query your cached FAISS index)
  - Upload New Document (PDF/EPUB) to parse, chunk, embed, and query on the fly  
- Modular `utils/` folder containing reusable ingestion, embedding, and query logic  
- Git-friendly repo: ignores heavy book files but keeps folder structure visible with .gitkeep  

---

## 🛠️ Tech Stack

- **Programming:** Python 3.9+  
- **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)  
- **Vector Database:** FAISS (IndexFlatL2)  
- **Reranking:** CrossEncoder (`ms-marco-MiniLM-L-12-v2`)  
- **Parsing:** pypdf, ebooklib, BeautifulSoup4  
- **LLM Inference:** Ollama (Mistral)  
- **Frontend:** Streamlit (interactive UI with document upload)  
- **Project Structure:** Modular utilities for maintainability (`utils/`)  

---

## 📂 Project Structure
```
knowledge-rag/
│
├── data/                # Place your PDF/EPUB books here (ignored by git)
│   └── .gitkeep
│
├── processed/           # Auto-generated plain text files (ignored by git)
│   └── .gitkeep
│
├── utils/               # Modular utility modules
│   ├── text_utils.py    # Parsing, cleaning, chunking
│   ├── embed_utils.py   # Embeddings, FAISS index build/load
│   └── query_utils.py   # Retrieval, reranking, Ollama integration
│
├── faiss_index.bin      # FAISS vector index (auto-generated, git-ignored)
├── mapping.json         # Mapping FAISS IDs to books/chunks
│
├── ingest.py            # Driver for ingestion & caching
├── embed.py             # Driver for embedding + FAISS index building
├── query.py             # Interactive CLI Q&A with Ollama
├── app.py               # Streamlit web app (pre-indexed mode + document upload)
├── requirements.txt     # Python dependencies
├── .gitignore           # Ignores venv, book files, caches
└── README.md            # Project documentation
```
---

## ⚙️ Setup Instructions

1. Clone the Repo  
   git clone https://github.com/yourusername/knowledge-rag.git  
   cd knowledge-rag  

2. Create Virtual Environment  
   python -m venv knowledge-rag-venv  
   knowledge-rag-venv\Scripts\Activate.ps1

3. Install Requirements  
   pip install -r requirements.txt  

4. Add Your Books  
   Place .pdf and .epub files into the data/ folder.  

5. Run Ingestion  
   python ingest.py  
   - First run: parses and caches text into processed/  
   - Later runs: loads from cache for speed  
   - Use force flag to re-ingest if needed:  
     python ingest.py force  

6. Build Embeddings and FAISS Index  
   python embed.py  

7. Run CLI Q&A  
   python query.py  
   - Type questions interactively  
   - Type `exit` to quit  

8. Run Streamlit App  
   streamlit run app.py  
   - Choose "Use Pre-Indexed Books" to query your library  
   - Choose "Upload New Document" to parse and query a new PDF/EPUB instantly  

---

## ✅ Example Query

**Question:** tell me about mesoamerica 

**Answer (via Ollama):**  
Mesoamerica, as described in the text, was a region where complex societies emerged during the last few centuries BC. By the first millennium AD, Mayan cities were growing in size and power, with vast public works being undertaken, temples and palaces being built, the arts flourishing, and the landscape being modified for planting. This pattern intensified in the first half of the 8th century AD, but thereafter, the Mayan civilization experienced a rapid collapse due to local production disasters. Scholars have suggested that this collapse may have been caused by factors such as soil erosion and land scarcity, encroachment of grasses, silting of lakes, decline of water supply in dry years, increase in mosquito populations, and possibly an invasion from northern barbarians. The collapse of the Highland city of Teotihuacan is also attributed to a similar scenario involving an invasion from barbarians who acculturated to Teotihuacan civilization.

**Sources:**  
1. The collapse of complex societi - Joseph A Tainter.txt (Score: 0.5630)
Preview: major concern to contemporary forecasters (e .g., Catton 19 80). Mesoamerica The spectacular collapse of Mayan civilization in the Southern Lowlands has frequently led scholars to focus on resource de...
------------------------------------------------------------
2. The collapse of complex societi - Joseph A Tainter.txt (Score: -0.4858)
Preview: B.C. By the last few centuries B.C. complex political organization and massive public architecture were emerging in many areas. Throughout most of the first millennium A.D. Mayan cities grew in size a...
------------------------------------------------------------
3. The collapse of complex societi - Joseph A Tainter.txt (Score: -0.9812)
Preview: local production disasters, collapse ensued (R. E. W. Adams 1971: 164, 197, 1973b: 152 ). Hove (19 81) has studied spatial trends in the cessation of stela (stone monument) construction across the Low...


---

## 🛠️ Next Steps

- [ ] Add support for merging uploaded documents with pre-indexed library  
- [ ] Provide configuration options for FAISS-only vs CrossEncoder reranked results  
- [ ] Optional: integrate OpenAI GPT fallback when Ollama is unavailable  
- [ ] Add demo screenshots/GIFs for GitHub presentation  

---

## 📌 Notes

- The data/ and processed/ folders are git-ignored to keep the repository lightweight.  
- Add your own PDF/EPUB books into the data/ folder for testing.  
- (🚫 not including books here because I’d rather not get sued 📚😂)