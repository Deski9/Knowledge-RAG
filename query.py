from utils.query_utils import retrieve_chunks, build_prompt, query_ollama

if __name__ == "__main__":
    print("📚 Knowledge-RAG Interactive Mode")
    print("Type your question, or 'exit' to quit.\n")

    while True:
        query = input("Your question: ")
        if query.lower().strip() == "exit":
            print("Goodbye 👋")
            break

        retrieved = retrieve_chunks(query, k=10, rerank_top=3)
        prompt = build_prompt(query, retrieved)

        try:
            answer = query_ollama(prompt)
        except Exception:
            answer = "⚠️ Ollama not running. Showing chunks only."

        print("\n--- Answer ---\n")
        print(answer)
        print("\n--- Sources ---")
        for rank, ((book, chunk), score) in enumerate(retrieved):
            print(f"{rank+1}. {book} (Score: {score:.4f})")
            print(f"Preview: {chunk[:200]}...")
            print("-" * 60)
