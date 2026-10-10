import pandas as pd
from chunking import chunks
from sentence_transformers import SentenceTransformer

# 1. Initialize the embedding model
embedding_model = SentenceTransformer(
    model_name_or_path="all-mpnet-base-v2",
    device="cpu"
)

# 2. Extract just the text strings from your dictionary into a flat list
text_to_embed = [item["chunk"] for item in chunks]

# 3. Generate the embeddings!
embeddings = embedding_model.encode(
    inputs=text_to_embed,
    batch_size=32
)

# 4. Attach the mathematical vectors back to your original dictionary
for i, item in enumerate(chunks):
    # We convert the numpy array to a standard Python list so it can be saved easily
    item["embedding"] = embeddings[i].tolist()

# 5. Save to a CSV file
df = pd.DataFrame(chunks)
save_path = r"C:\Users\HP\OneDrive\Documents\Repos\ai-engineering-mastery\rag-from-scratch\02\data\text_chunks_and_embeddings.csv"
df.to_csv(save_path, index=False)
print("Document Embedding Done.")