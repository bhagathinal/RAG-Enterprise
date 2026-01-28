# --------------------------------------------------
# Import PyPDFLoader from LangChain
# This loader is used to read PDF files and convert
# them into LangChain Document objects
# --------------------------------------------------
from langchain_community.document_loaders import PyPDFLoader 

# --------------------------------------------------
# Function to load documents from a given file path
# --------------------------------------------------
def load_documents(file_path):

    """
    Loads PDF documents from the specified file path.

    Parameters:
    file_path (str):
        - Path to the PDF file or directory containing PDFs

    Returns:
    documents (List[Document]):
        - A list of LangChain Document objects
        - Each document contains:
            - page_content (text)
            - metadata (source, page number)
    """

    # Initialize the PDF loader with the provided path
    loader = PyPDFLoader(file_path)

    # Load and parse the PDF files into Document objects
    documents = loader.load()

    # Return the extracted documents
    return documents
