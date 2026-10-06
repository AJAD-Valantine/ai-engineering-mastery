from ingest import collection
from openai import APIConnectionError, OpenAI

client = OpenAI(base_url="http://localhost:11434/v1" , api_key="ollama")

system_prompt = """
        Based on the following context and conversation history, 
        please provide a relevant and contextual response. If the answer cannot 
        be derived from the context, only use the conversation history or say 
        "I cannot answer this based on the provided information."
                """

messages = [
    {"role": "system", "content": system_prompt},
]

while True:

    query = input("Enter your query: ").strip().lower()

    if query == "exit":
        break
    if query == "new":
        print("Chat cleared.")
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        continue

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    context = "\n".join(results["documents"][0])

    prompt = f"""
    
        Context from documents: 
        
        {context}
    
        Human: 

        {query}
    
            """


    messages.append(
        {
            "role" : "user",
            "content" : prompt
        }
    )

    try:
        result = client.chat.completions.create(
            model="llama3.2", messages=messages, temperature=0, stream=True
        )

        full_text = ""
        for line in result:
            chunk = line.choices[0].delta.content

            if chunk:
                print(chunk, end="", flush=True)
                full_text += chunk
        print()
    except APIConnectionError:
        print("Error occurred")
        break

    messages.append({"role": "assistant", "content": full_text})