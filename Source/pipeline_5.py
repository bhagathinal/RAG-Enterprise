from Source.loader import load_documents
from Source.vector_store_5 import create_vector_store
from Source.llm_5 import load_llm
from langchain.chains import RetrievalQA

VECTORSTORE = None

def initialize_pieline():
    global VECTORSTORE
    documents = load_documents("Data")
    VECTORSTORE = create_vector_store(documents)

def run_pipeline(question):
    global VECTORSTORE

    if VECTORSTORE is None:
        initialize_pieline()

    llm = load_llm()
    retriever = VECTORSTORE.as_retriever(search_kwargs={"k":3})

    qa = RetrievalQA.grom_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    result = qa(question)

    sources = []
    for doc in result["source_documents"]:
        sources.append({
            "source" : doc.metadata.get("source","Document"),
            "page" : doc.metadata.get("page","N/A")
        })

    return {
        "answer" : result["result"],
        "sources" : sources
    }