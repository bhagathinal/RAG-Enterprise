def process_question(question: str) -> str:
    """
    This function performs minimal preprocessing on the user question.

    WHY minimal?
    - We do NOT use keywords
    - We do NOT use synonym lists
    - We do NOT use rule-based logic

    All semantic understanding is handled by embeddings later.

    Enterprise principle:
    "Do as little as possible before embeddings"
    """
    
    # Remove leading and trailing spaces
    # Convert to lowercase for consistency
    return question.strip().lower()
