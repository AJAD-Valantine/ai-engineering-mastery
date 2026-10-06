from openai import OpenAI, APIConnectionError

model = "llama3.2"
url = "http://localhost:11434/v1"
api_key = "ollama"
temperature = 0.3
system_prompt = "You are a CS professor"

CONFIG = {
    "model" : model,
    "base_url" : url,
    "api_key" : api_key,
    "temperature" : temperature,
    "system_prompt" : system_prompt
}

client = OpenAI(
    base_url=CONFIG["base_url"],
    api_key=CONFIG["api_key"],
)

messages = [
    {
        "role": "system",
        "content": CONFIG["system_prompt"]
    }
]

while True:

    prompt = input("Enter your message: ")

    if not prompt:
        continue
    if prompt.lower() == "/exit":
        break
    if prompt.lower() == "/help":
        print("""
            /help - get commands
            /new - start a new chat
            /exit - exit the chat
        """)
        continue
    if prompt.lower() == "/new":
        messages = [
            {
                "role": "system",
                "content": CONFIG["system_prompt"]
            }
        ]
        continue

    messages.append({
        "role" : "user",
        "content" : prompt
     })

    try:
        response = client.chat.completions.create(
            model=CONFIG["model"],
            temperature=CONFIG["temperature"],
            messages=messages,
            stream=True,
            timeout=30,
        )

        full_text = ""
        for line in response:
            chunk = line.choices[0].delta.content

            if chunk:
                print(chunk, end="", flush=True)
                full_text += chunk
        print()

        messages.append({"role" : "assistant", "content" : full_text})

    except APIConnectionError:
        print("A connection error occurred")
        messages.pop()
        continue