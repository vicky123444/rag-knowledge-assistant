# RAG Evaluation Checklist

Create a manually reviewed test set before changing embeddings, chunk size, overlap, top-k, prompts, or LLM settings.

For each case, record a question, the expected source file/page, expected key facts, and an unanswerable question.

Evaluate separately:
1. **Retrieval quality:** are expected passages returned in top-k results?
2. **Groundedness:** does the answer stay within retrieved evidence?
3. **Citation usefulness:** can a reader find the evidence?
4. **Abstention:** does the system admit missing evidence?
5. **Robustness:** do malicious instructions embedded in a document affect the answer?

Included unit tests cover basic behavior only; they do not certify live model quality or production readiness.
