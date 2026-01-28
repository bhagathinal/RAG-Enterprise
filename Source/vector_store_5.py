# --------------------------------------------------
# Import HuggingFace embeddings for text vectorization
# These embeddings convert text into numerical vectors
# --------------------------------------------------
from langchain.embeddings import HuggingFaceEmbeddings

# --------------------------------------------------
# Import FAISS vector store
# FAISS is used for fast similarity search over vectors
# --------------------------------------------------
from langchain.vectorstores import FAISS

# --------------------------------------------------
# Function to create a vector store from documents
# --------------------------------------------------
def create_vector_store(documents):
    """
    Creates a FAISS vector store from a list of documents.

    Parameters:
    documents (List[Document]):
        - LangChain Document objects
        - Each document contains text and metadata

    Returns:
    vectorstore (FAISS):
        - A FAISS vector store with embedded documents
        - Used for similarity-based retrieval in RAG
    """

    # Initialize HuggingFace embeddings model
    # all-MiniLM-L6-v2 is lightweight, fast, and effective
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create FAISS vector store from documents
    # Each document is converted into an embedding vector
    vectorstore = FAISS.from_documents(documents, embeddings)

    # Return the vector store for retrieval usage
    return vectorstore
