from openai import OpenAI

MODEL = "llama3.2"
url = "http://localhost:11434/v1"

client = OpenAI(
    base_url=url,
    api_key="ollama",
)

messages = [
    {
        "role" : "system",
        "content" : "You are a CS professor"
    }
]

while True:

    prompt = input("Enter your message: ")

    if not prompt:
        continue
    if prompt.lower() == "exit":
        break

    messages.append({
        "role" : "user",
        "content" : prompt
     })

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True,
        temperature=0.3,
    )

    full_text = ""
    for line in response:
        chunk = line.choices[0].delta.content

        if chunk:
            print(chunk, end="", flush=True)
            full_text += chunk
    print()

    messages.append({"role" : "assistant", "content" : full_text})