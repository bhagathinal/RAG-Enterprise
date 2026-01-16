import json
import re
from pathlib import Path
from access_control.permissions import DOMAIN_ROLE_MAPPING

# -----------------------------
# Paths (MATCH pdf_parsing.py)
# -----------------------------
PARSED_PATH = Path("Data/parsed/parsed_documents.json")
OUTPUT_PATH = Path("Data/processed/cleaned_documents.json")

# Ensure output directory exists
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Domain detection logic
# -----------------------------
def detect_domain(filename: str) -> str:
    """
    Detects document domain based on filename keywords
    """
    name = filename.lower()

    if "handbook" in name or "leave" in name:
        return "HR"
    elif "annual" in name or "financial" in name or "report" in name:
        return "Finance"
    elif "technical" in name or "technology" in name or "kubernetes" in name:
        return "Technical"
    else:
        return "General"


# -----------------------------
# Text cleaning function
# -----------------------------
def clean_text(text: str) -> str:
    """
    Cleans extracted PDF text by removing newlines
    and extra spaces
    """
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -----------------------------
# Main processing function
# -----------------------------
def main():
    # Load parsed PDF text
    with open(PARSED_PATH, "r", encoding="utf-8") as f:
        parsed_documents = json.load(f)

    cleaned_docs = []

    for doc in parsed_documents:
        # Use correct key name: "source"
        domain = detect_domain(doc["source"])

        cleaned_docs.append({
            "text": clean_text(doc["text"]),
            "source": doc["source"],
            "page": doc["page"],
            "domain": domain,
            "allowed_roles": DOMAIN_ROLE_MAPPING.get(domain, [])
        })

    # Save cleaned documents
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(cleaned_docs, f, indent=2, ensure_ascii=False)

    print("✅ Text cleaning and tagging completed.")


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    main()
