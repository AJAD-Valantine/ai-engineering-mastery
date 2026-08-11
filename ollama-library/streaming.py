import ollama


MODEL = "llama3.2"

prompt = input("Enter your prompt: ")

messages = [
    {
        "role" : "user",
        "content" : prompt
     }
]


response = ollama.chat(
    model=MODEL,
    messages=messages,
    stream=True
)

for line in response:
    chunk = line["message"]["content"]
    print(chunk, flush=True, end="")