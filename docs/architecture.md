# Architecture

The application separates retrieval from generation:

1. **Ingestion** extracts text from PDF, TXT, and Markdown.
2. **Chunking** creates overlapping character windows and preserves filename and page metadata.
3. **Embeddings** convert text and questions to vectors using a local sentence-transformer model.
4. **Vector storage** persists vectors and metadata in ChromaDB.
5. **Retrieval** selects the top-k matching passages.
6. **Prompt construction** passes the question and retrieved evidence to the LLM while treating documents as untrusted input.
7. **Generation** produces an answer and returns excerpts from the retrieved sources.

This is an educational single-user starter. Authentication, tenant isolation, update/delete APIs, OCR, asynchronous ingestion, quotas, and production monitoring are not included.
