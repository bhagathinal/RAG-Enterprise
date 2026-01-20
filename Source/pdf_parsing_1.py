import json
from pathlib import Path
from pypdf import PdfReader

# -----------------------------
# Define paths
# -----------------------------

# Folder where raw PDF files are stored
RAW_DATA_PATH = Path("Data/raw")

# Output JSON file path
PARSED_FILE_PATH = Path("Data/parsed/parsed_documents.json")

# Ensure the parent directory (Data/parsed) exists
PARSED_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Function to parse PDFs
# -----------------------------
def parse_pdfs():
    """
    Reads all PDF files from RAW_DATA_PATH,
    extracts text page-by-page,
    and saves the output as a structured JSON file.
    """

    # This list will store all extracted text chunks
    documents = []

    # Loop through all PDF files in the raw data folder
    for pdf_file in RAW_DATA_PATH.glob("*.pdf"):

        print(f"Parsing: {pdf_file.name}")

        # Load the PDF
        reader = PdfReader(pdf_file)

        # Loop through each page in the PDF
        for page_number, page in enumerate(reader.pages, start=1):

            # Extract text from the page
            text = page.extract_text()

            # Only store pages that contain text
            if text and text.strip():
                documents.append({
                    "text": text.strip(),      # Page content
                    "source": pdf_file.name,   # Which file it came from
                    "page": page_number        # Page number
                })

    # -----------------------------
    # Save extracted data to JSON
    # -----------------------------
    with open(PARSED_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)

    print("✅ PDF parsing completed successfully!")
    print(f"📄 Total pages extracted: {len(documents)}")


# -----------------------------
# Script entry point
# -----------------------------
if __name__ == "__main__":
    parse_pdfs()
