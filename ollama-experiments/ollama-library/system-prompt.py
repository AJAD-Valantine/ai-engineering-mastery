import ollama


MODEL = "llama3.2"
system_prompt = "you are a computer science teacher"

messages = [
    {"role" : "system", "content" : system_prompt}
]

while True:

    prompt = input("Enter your prompt: ")

    if not prompt:
        continue
    if prompt == "exit":
        break

    messages.append({"role" : "user", "content" : prompt})

    response = ollama.chat(
        model=MODEL,
        messages=messages,
        stream=True
    )

    full_response = ""
    for line in response:
        chunk = line["message"]["content"]
        print(chunk, flush=True, end="")
        full_response += chunk
    print()

    messages.append({"role" : "assistant", "content" : full_response})
