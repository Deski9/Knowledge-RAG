# Knowledge-RAG

A prototype Retrieval-Augmented Generation (RAG) system for querying books and documents.  
This project demonstrates ingestion, caching, and preprocessing of PDF and EPUB books to prepare for semantic search and LLM-based question answering.

---

## 🚀 Current Features

- Environment setup with a dedicated Python virtual environment  
- Book ingestion supporting both PDF and EPUB formats  
- Caching system: saves parsed `.txt` files in processed/ so ingestion only runs once per book  
- Text cleaning: normalizes whitespace (removes tabs, multiple spaces, and line breaks)  
- Chunking of ingested text into overlapping sections for semantic embeddings  
- FAISS vector store built from book embeddings for efficient similarity search  
- Git-friendly repo: ignores heavy book files but keeps folder structure visible with .gitkeep 

---

## 🛠️ Tech Stack

- **Programming:** Python 3.9+  
- **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)  
- **Vector Database:** FAISS (IndexFlatL2)  
- **Parsing:** pypdf, ebooklib, BeautifulSoup4  
- **Environment:** Virtualenv, Git  
- **LLM Inference (planned):** Ollama (local models such as Mistral)  
- **Frontend (planned):** Streamlit for interactive Q&A  

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
├── faiss_index.bin      # FAISS vector index (auto-generated, git-ignored)
├── mapping.json         # Mapping FAISS IDs to books/chunks
│
├── ingest.py            # Script to parse and cache book content
├── embed.py             # Script to chunk text, embed, and build FAISS index
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

   - Creates faiss_index.bin and mapping.json  
   - Includes a sample test query to verify retrieval  
---

## ✅ Example Output

Query: Who is Judge Holden?

Result 1:
Book: Blood Meridian, Or, the Evening - Cormac McCarthy.txt
Chunk: placed his elbows on the bar behind him. Watching him across the layered smoke in the yellow light was the judge...
Distance: 1.2314
---

## 🛠️ Next Steps

- [ ] Add semantic retrieval + Ollama integration  
- [ ] Streamlit UI for interactive Q&A  

---

## 📌 Notes

- The `data/` and `processed/` folders are git-ignored to keep the repository lightweight.  
- Add your own PDF/EPUB books into the `data/` folder for testing.  
- (🚫 not including books here because I’d rather not get sued 📚😂)
