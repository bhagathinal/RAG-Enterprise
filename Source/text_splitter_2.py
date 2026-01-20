import json
from pathlib import Path

# -----------------------------
# File paths
# -----------------------------
INPUT_PATH = Path("Data/processed/cleaned_documents.json")
OUTPUT_PATH = Path("Data/processed/chunked_documents.json")

# Ensure output directory exists
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Chunking configuration
# -----------------------------
CHUNK_SIZE = 400     # number of words per chunk
OVERLAP = 50         # overlapping words between chunks


# -----------------------------
# Text chunking function
# -----------------------------
def chunk_text(text: str):
    """
    Splits text into overlapping word-based chunks.
    """
    words = text.split()
    chunks = []

    step = CHUNK_SIZE - OVERLAP

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + CHUNK_SIZE])
        chunks.append(chunk)

    return chunks


# -----------------------------
# Main processing function
# -----------------------------
def main():
    # Load cleaned documents
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        documents = json.load(f)

    chunked_docs = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for idx, chunk in enumerate(chunks):
            chunked_docs.append({
                "chunk_text": chunk,
                "chunk_id": idx,
                "source": doc["source"],
                "page": doc["page"],
                "domain": doc["domain"],
                "allowed_roles": doc["allowed_roles"]
            })

    # Save chunked output
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunked_docs, f, indent=2, ensure_ascii=False)

    print("✅ Text chunking completed successfully.")


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    main()
