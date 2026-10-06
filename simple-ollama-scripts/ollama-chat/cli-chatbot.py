import requests
import json

url = "http://localhost:11434/api/chat"
MODEL = "llama3.2"

system_prompt = "You are a intelligent chatbot"

json_body = {
    "model": MODEL,
    "messages": [
        {"role" : "system", "content" : system_prompt}
    ],
    "stream": True
}

print("""
    Commands:
    /new
    /exit
    """)

print("Welcome to a new chat!")

while True:

    prompt = input("You: ")

    if not prompt:
        continue
    if prompt == "/exit":
        break
    if prompt == "/new":
        print("Byeee")
        json_body = {
            "model": MODEL,
            "messages": [
                {"role" : "system", "content" : system_prompt}
            ],
            "stream": True
        }
        print("Welcome to a new chat!")
        prompt = input("You: ")

    json_body["messages"].append({"role" : "user", "content" : prompt})

    response = requests.post(
        url=url,
        json=json_body,
        stream=True,
    )

    full_response = ""
    print("Bot: ", end="", flush=True)
    if response.status_code == 200:
        for line in response.iter_lines():
            line = line.decode("utf-8")
            chunk = json.loads(line)
            print(chunk["message"]["content"], flush=True, end="")

            full_response += chunk["message"]["content"]
            json_body["messages"].append({"role" : "assistant", "content" : full_response})

        print()

    else:
        print(response.status_code, response.text)
        break