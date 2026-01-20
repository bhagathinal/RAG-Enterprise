from prompts import load_system_prompt


def build_context(retrieved_chunks: list) -> str:
    """
    Combine retrieved document chunks into a single context block.

    Args:
        retrieved_chunks (list): Output from retrieval phase

    Returns:
        str: Context text for LLM
    """

    context_blocks = []

    for chunk in retrieved_chunks:
        context_blocks.append(
            f"[Source: {chunk['source']} | Page: {chunk['page']}]\n"
            f"{chunk['text']}"
        )

    return "\n\n".join(context_blocks)


def build_messages(question: str, retrieved_chunks: list) -> list:
    """
    Build messages for LLM API call.

    Args:
        question (str): User question
        retrieved_chunks (list): Retrieved chunks from FAISS

    Returns:
        list: Messages formatted for LLM API
    """

    # Domain inferred from top chunk (industry standard approach)
    domain = retrieved_chunks[0].get("domain", "general")

    system_prompt = load_system_prompt(domain)

    user_prompt = f"""
Context:
{build_context(retrieved_chunks)}

Question:
{question}

Answer ONLY using the above context.
If the answer is not present, say so clearly.
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
