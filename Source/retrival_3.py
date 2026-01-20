# ================================
# IMPORT REQUIRED LIBRARIES
# ================================

import json                      # Used to load metadata stored as JSON
import faiss                     # Used for fast vector similarity search
import numpy as np               # Used for numerical operations
from pathlib import Path         # Used for OS-independent file paths
from sentence_transformers import SentenceTransformer  # Embedding model
from question_processing_3 import process_question     # Custom question cleaner


# ================================
# PATH CONFIGURATION
# ================================

# Path where FAISS vector index is stored
FAISS_INDEX_PATH = Path("Data/faiss/index.faiss")

# Path where metadata (text, source, page info, etc.) is stored
METADATA_PATH = Path("Data/faiss/metadata.json")


# ================================
# LOAD EMBEDDING MODEL
# ================================

# This model converts text into numerical vectors (embeddings)
# It understands semantic meaning, not keywords
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(EMBEDDING_MODEL_NAME)


# ================================
# RETRIEVAL FUNCTION
# ================================

def retrieve(question: str, top_k: int = 5):
    """
    Takes a natural language question
    Returns top_k most relevant document chunks using vector similarity
    """

    # ----------------------------
    # Load FAISS index from disk
    # ----------------------------
    index = faiss.read_index(str(FAISS_INDEX_PATH))

    # ----------------------------
    # Load metadata corresponding to FAISS vectors
    # Each FAISS index position maps to one metadata entry
    # ----------------------------
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # ----------------------------
    # Process / clean the question
    # (lowercasing, removing noise, etc.)
    # ----------------------------
    processed_question = process_question(question)

    # ----------------------------
    # Convert question into embedding
    # Shape: (embedding_dim,)
    # ----------------------------
    query_vector = model.encode(processed_question).astype("float32")

    # ----------------------------
    # Normalize vector (important for cosine similarity)
    # ----------------------------
    faiss.normalize_L2(query_vector.reshape(1, -1))

    # ----------------------------
    # Perform similarity search in FAISS
    # Returns:
    # scores  -> distance/similarity values
    # indices -> positions of matched documents
    # ----------------------------
    score, indices = index.search(
        query_vector.reshape(1, -1),
        top_k
    )

    # ----------------------------
    # Collect retrieved results
    # ----------------------------
    results = []

    for idx, score in zip(indices[0], score[0]):
        doc = metadata[idx]   # Fetch corresponding metadata

        results.append({
            "text": doc["text"],                 # Retrieved content
            "source": doc["source"],             # Document source
            "page": doc["page"],                 # Page number
            "domain": doc["domain"],             # Business domain
            "allowed_roles": doc["allowed_roles"],  # Access control
            "score": float(score)                # Similarity score
        })

    return results


# ================================
# RUN FILE DIRECTLY (TEST MODE)
# ================================

if __name__ == "__main__":

    # Sample user query (no keywords required)
    query = "How many leaves do employees get?"

    # Retrieve top 5 relevant chunks
    results = retrieve(query, top_k=5)

    # Print results
    for r in results:
        print("-" * 60)
        print("Score:", r["score"])
        print("Source:", r["source"], "Page:", r["page"])
        print(r["text"][:300])   # Print first 300 characters
