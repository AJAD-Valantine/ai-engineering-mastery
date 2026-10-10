import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

DATA_PATH = Path(
    r"C:\Users\HP\OneDrive\Documents\Repos\ai-engineering-mastery\rag-from-scratch\02\data\text_chunks_and_embeddings.csv"
)

df = pd.read_csv(DATA_PATH)
df["embedding"] = df["embedding"].apply(json.loads)

pages_and_chunks = df.to_dict(orient="records")
embeddings_tensor = torch.tensor(
    np.array(df["embedding"].tolist()), dtype=torch.float32
)

embedding_model = SentenceTransformer("all-mpnet-base-v2", device="cpu")


def retrieve_context(
    query: str,
    top_k: int = 5,
    embeddings: torch.Tensor = embeddings_tensor,
    chunks_list=None,
    model: SentenceTransformer = embedding_model,
) -> list[dict]:

    if chunks_list is None:
        chunks_list = pages_and_chunks

    query_embedding = model.encode(inputs=query, convert_to_tensor=True)

    dot_scores = util.dot_score(query_embedding, embeddings)[0]
    scores, indices = torch.topk(input=dot_scores, k=top_k)

    retrieved_items = []
    for score, idx in zip(scores, indices):
        item = dict(chunks_list[idx])
        item["score"] = float(score)
        retrieved_items.append(item)

    return retrieved_items