from Source.loader_5 import load_documents
from Source.vector_store_5 import create_vector_store
from Source.llm_5 import load_llm

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

VECTORSTORE = None


def initialize_pipeline():
    """Load documents and build vector store once"""
    global VECTORSTORE

    documents = load_documents("Data")
    print(f"📄 Documents loaded: {len(documents)}")

    VECTORSTORE = create_vector_store(documents)
    print("✅ Vector store created")


def format_docs(docs):
    """Convert documents into plain text for prompt"""
    return "\n\n".join(doc.page_content for doc in docs)


def run_pipeline(question: str):
    """Main RAG pipeline"""
    global VECTORSTORE

    if VECTORSTORE is None:
        initialize_pipeline()

    llm = load_llm()
    retriever = VECTORSTORE.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_template(
        """
        You are an enterprise AI assistant.
        Answer ONLY using the context below.
        If the answer is not found, say:
        "Not available in company documents."

        Context:
        {context}

        Question:
        {question}
        """
    )

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = rag_chain.invoke(question)

    # fetch sources separately (for UI)
    source_docs = retriever.invoke(question)

    return {
        "answer": answer,
        "sources": [doc.metadata for doc in source_docs]
    }
