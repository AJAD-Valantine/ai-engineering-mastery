def prompt_formatter(
        query: str,
        context_items: list[dict]
        ) -> str:

    """Formats retrieved chunks and user query into an augmented prompt."""

    context: str = "- " + "\n- ".join([item["chunk"] for item in context_items])

    base_prompt: str = f"""
                Based on the following context items, please answer the query.
                Extract relevant information directly from the context before answering.
                Answer accurately and concisely.
                If the context does not contain enough information, state that clearly.

                Context:
                {context}

                User query: {query}
                Answer:
                        """

    return base_prompt
