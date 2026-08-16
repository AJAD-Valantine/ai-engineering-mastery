import chromadb
from chromadb.utils import embedding_functions

# LOAD
file_path = "knowledge.txt"
file = open(file_path, "r")  # noqa: SIM115
text = file.read()

# SPLIT
sentences = text.replace("\n", " ").split(".")

char_limit_in_chunk = 250
completed_chunks = [] # finished chunks
current_chunk = "" # current working chunk
current_chunk_size = 0 # how many chars are inside the current chunk

for sentence in sentences:

    sentence = sentence.strip()

    if not sentence:
        continue
    if not sentence.endswith("."):
        sentence += ". "

    sentence_length = len(sentence)

    if (current_chunk_size + sentence_length > char_limit_in_chunk) and current_chunk:
        completed_chunks.append(current_chunk)
        current_chunk = sentence

    else:
        current_chunk += sentence

    current_chunk_size = len(current_chunk)

if current_chunk:
    completed_chunks.append(current_chunk)

metadata = [{"source": file_path, "chunk": i} for i in range(len(completed_chunks))]
ids = [f"{file_path}_chunk_{i}" for i in range(len(completed_chunks))]

# EMBED
client = chromadb.PersistentClient(path="chroma_db")

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="documents_collection",
    embedding_function=sentence_transformer_ef
)

# STORE
collection.add(
    ids=ids,
    metadatas=metadata,
    documents=completed_chunks
)