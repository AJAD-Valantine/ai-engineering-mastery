from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyMuPDF4LLMLoader(
    r"C:\Users\HP\OneDrive\Documents\Repos\ai-engineering-mastery\rag-from-scratch\data\Human_Nutrition.pdf"
)

loaded_data: list[Document] = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

chunks: list[Document] = text_splitter.split_documents(loaded_data)

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vector_db = Chroma.from_documents(
    chunks,
    embeddings,
)

query = "List down the vitamins I should use for my skin."

retriever = vector_db.as_retriever()

prompt = ChatPromptTemplate.from_template("""
Answer the question using only the provided context.

Context:
{context}

Question:
{question}
""")

model = ChatOllama(model="llama3.1:8b")



chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough(),
    }
    | prompt
    | model
    | StrOutputParser()
)
