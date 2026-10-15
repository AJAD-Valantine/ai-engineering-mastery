import os

from langchain_ollama import ChatOllama

llm = ChatOllama(
    model=os.environ.get("LLM_MODEL", "llama3.1:8b"),
    temperature=0.3,
    num_predict=1500,
)
