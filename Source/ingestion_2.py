import json
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# -----------------------------
# Paths
# -----------------------------

# Input: output of Phase 1 (text_splitter.py)
CHUNKS_PATH = Path("Data/processed/chunked_documents.json")

# Output directories
FAISS_DIR = Path("Data/faiss")
FAISS_INDEX_PATH = FAISS_DIR / "index.faiss"
METADATA_PATH = FAISS_DIR / "metadata.json"

FAISS_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Embedding Model
# -----------------------------
# Industry standard, fast, high quality
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# -----------------------------
# Main Ingestion Logic
# -----------------------------

def main():
    # Load chunked documents
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        raise ValueError("No chunks found. Check Phase 1 output.")

    embeddings = []
    metadata = []

    # Generate embeddings
    for chunk in tqdm(chunks, desc="Generating embeddings"):
        vector = model.encode(chunk["chunk_text"])

        embeddings.append(vector)
        metadata.append({
            "text": chunk["chunk_text"],
            "source": chunk["source"],
            "page": chunk["page"],
            "domain": chunk["domain"],
            "allowed_roles": chunk["allowed_roles"]
        })

    # Convert to numpy array (FAISS requirement)
    embeddings_np = np.array(embeddings).astype("float32")

    # -----------------------------
    # Build FAISS Index
    # -----------------------------
    dimension = embeddings_np.shape[1]

    # Inner Product = cosine similarity (normalized embeddings)
    index = faiss.IndexFlatIP(dimension)

    # Normalize vectors for cosine similarity
    faiss.normalize_L2(embeddings_np)
    index.add(embeddings_np)

    # Save index to disk
    faiss.write_index(index, str(FAISS_INDEX_PATH))

    # Save metadata separately
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("Ingestion completed successfully")
    print(f"FAISS index size: {index.ntotal} vectors")


if __name__ == "__main__":
    main()
