# --------------------------------------------------
# Import document loader
# Responsible for reading documents from disk
# and converting them into LangChain Document objects
# --------------------------------------------------
from Source.loader_5 import load_documents

# --------------------------------------------------
# Import vector store creation logic
# Builds embeddings and stores them in a vector database
# --------------------------------------------------
from Source.vector_store_5 import create_vector_store

# --------------------------------------------------
# Import LLM loader
# Loads and configures the language model (OpenAI / local / HuggingFace)
# --------------------------------------------------
from Source.llm_5 import load_llm

# --------------------------------------------------
# LangChain RetrievalQA chain
# Combines retrieval + LLM generation into one pipeline
# --------------------------------------------------
from langchain.chains import RetrievalQA


# --------------------------------------------------
# Global variable to store the vector store in memory
# This avoids rebuilding embeddings on every query
# --------------------------------------------------
VECTORSTORE = None


# --------------------------------------------------
# Initialize the full RAG pipeline
# - Load documents
# - Create vector store
# - Cache it globally
# --------------------------------------------------
def initialize_pipeline():
    global VECTORSTORE

    # Load documents from the Data directory
    documents = load_documents("Data")

    # Create vector store from documents
    VECTORSTORE = create_vector_store(documents)


# --------------------------------------------------
# Run the RAG pipeline for a user question
# --------------------------------------------------
def run_pipeline(question):
    global VECTORSTORE

    # Ensure vector store is initialized
    if VECTORSTORE is None:
        initialize_pipeline()

    # Load the language model
    llm = load_llm()

    # Convert vector store into a retriever
    # k=3 → retrieve top 3 most relevant chunks
    retriever = VECTORSTORE.as_retriever(search_kwargs={"k": 3})

    # Build RetrievalQA chain
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    # Execute the chain with the user's question
    result = qa(question)

    # --------------------------------------------------
    # Extract source metadata for transparency
    # --------------------------------------------------
    sources = []
    for doc in result["source_documents"]:
        sources.append({
            "source": doc.metadata.get("source", "Document"),
            "page": doc.metadata.get("page", "N/A")
        })

    # --------------------------------------------------
    # Return final structured response
    # --------------------------------------------------
    return {
        "answer": result["result"],
        "sources": sources
    }
