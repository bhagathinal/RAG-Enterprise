from langchain.documnet_loaders import PyPDFLoader

def load_documents(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents