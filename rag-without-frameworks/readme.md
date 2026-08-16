# Simple Local RAG Pipeline

A barebones, framework-free Retrieval-Augmented Generation (RAG) pipeline built entirely from scratch in Python. 
This project demonstrates the core mechanics of RAG—document loading, manual chunking, embedding generation, vector storage, and context augmentation—without relying on abstraction layers like LangChain or LlamaIndex.

## Features
- **Manual Text Chunking:** Custom logic to split `.txt` files by sentence while respecting character limits.
- **Local Vector Database:** Uses ChromaDB for persistent, local storage of embeddings.
- **Local Embeddings:** Generates vector embeddings locally using `sentence-transformers` (`all-MiniLM-L6-v2`).
- **Local LLM Integration:** Uses the `openai` Python client to connect to a locally hosted Ollama instance running `llama3.2`.
- **Streaming Responses:** Streams the LLM output to the terminal just like ChatGPT.
- **Conversation Memory:** Maintains chat history for contextual follow-up questions.