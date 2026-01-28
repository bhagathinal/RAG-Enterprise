def validate_answer(answer: str, retrieved_chunks: list) -> bool:
    """
    Simple faithfulness check:
    Answer words must overlap with retrieved context
    """

    combined_context = " ".join([c["text"] for c in retrieved_chunks]).lower()
    answer_words = set(answer.lower().split())

    overlap = sum(1 for w in answer_words if w in combined_context)

    # Threshold can be tuned
    return overlap / max(len(answer_words), 1) > 0.3
