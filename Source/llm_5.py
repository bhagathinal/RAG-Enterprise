# --------------------------------------------------
# Import OpenAI LLM wrapper from LangChain
# This provides a standardized interface to interact
# with OpenAI language models inside LangChain pipelines
# --------------------------------------------------
from langchain_community.llms import OpenAI


# --------------------------------------------------
# Function to load and configure the LLM
# --------------------------------------------------
def load_llm():
    """
    Loads the Language Model used for answer generation.

    Why temperature = 0?
    - Ensures deterministic responses
    - Reduces hallucinations
    - Preferred for enterprise and policy-based systems
    """

    return OpenAI(
        temperature=0  # Lower temperature = more factual & consistent answers
    )
