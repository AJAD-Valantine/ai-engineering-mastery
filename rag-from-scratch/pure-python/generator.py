from augmentor import prompt_formatter
from openai import OpenAI
from retriever import retrieve_context

# ==========================================
# 1. CONFIGURATION & CLIENT
# ==========================================
CONFIG = {
    "model": "llama3.2",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
    "temperature": 0.1,
    "system_prompt": (
        "You are a Retrieval-Augmented Generation (RAG) assistant. "
        "Your job is to answer the user's questions accurately using the information "
        "provided in the retrieved context. If the answer cannot be found in the context, "
        "state that clearly."
    ),
}

client = OpenAI(
    base_url=CONFIG["base_url"],
    api_key=CONFIG["api_key"],
)


# ==========================================
# 2. STANDALONE PIPELINE FUNCTION
# ==========================================
def generate_rag_response(query: str, top_k: int = 5) -> dict:
    """
    Executes the full RAG pipeline for a single query.
    Returns a dictionary containing the query, answer, and retrieved contexts.
    """
    # 1. Retrieve chunks
    retrieved_items = retrieve_context(query=query, top_k=top_k)

    # 2. Extract plain text chunks for RAGAS evaluation
    context_texts = [item["chunk"] for item in retrieved_items]

    # 3. Format augmented prompt
    augmented_prompt = prompt_formatter(query=query, context_items=retrieved_items)

    # 4. Generate answer from LLM
    response = client.chat.completions.create(
        model=CONFIG["model"],
        temperature=CONFIG["temperature"],
        messages=[
            {"role": "system", "content": CONFIG["system_prompt"]},
            {"role": "user", "content": augmented_prompt}
        ],
        stream=False,  # Set to False so we get the complete string back at once
        timeout=60,
    )

    model_answer = response.choices[0].message.content

    return {
        "question": query,
        "answer": model_answer,
        "contexts": context_texts
    }


# ==========================================
# 3. INTERACTIVE CLI
# ==========================================
if __name__ == "__main__":
    print("--- Interactive Chat Mode ---")
    print("Type '/exit' to quit.\n")

    while True:

        try:
            query = input("\nEnter your query: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting chat. Goodbye!")
            break

        if not query:
            print("Query cannot be empty.")
            continue

        if query.lower() == "/exit":
            print("Exiting chat. Goodbye!")
            break

        result = generate_rag_response(query)

        print("\nQuestion:\n", query)
        print("\nAnswer:\n", result["answer"])