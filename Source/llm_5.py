from langchain.llms import OpenAI

def load_llm():
    return OpenAI(temperature = 0)