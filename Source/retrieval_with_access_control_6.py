import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Paths
FAISS_INDEX_PATH = Path("Data/faiss/index.faiss")
METADATA_PATH = Path("Data/faiss/metadata.json")

# Embedding model (same as ingestion)
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_with_access_control(question: str, user_role: str, top_k: int = 5):
    """
    Retrieves relevant chunks and filters them based on user role
    """

    # Load FAISS index
    index = faiss.read_index(str(FAISS_INDEX_PATH))

    # Load metadata
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Encode question
    query_vector = model.encode(question).astype("float32")
    faiss.normalize_L2(query_vector.reshape(1, -1))

    # Retrieve more results than needed (buffer)
    scores, indices = index.search(query_vector.reshape(1, -1), top_k * 3)

    authorized_results = []

    for idx, score in zip(indices[0], scores[0]):
        doc = metadata[idx]

        # 🔐 Access Control Check
        if user_role in doc.get("allowed_roles", []):
            authorized_results.append({
                "text": doc["text"],
                "source": doc["source"],
                "page": doc["page"],
                "domain": doc["domain"],
                "score": float(score)
            })

        if len(authorized_results) >= top_k:
            break

    return authorized_results
