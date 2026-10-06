import requests

url = "http://localhost:11434/api/chat"
MODEL = "llama3.2"

json_body = {
    "model": MODEL,
    "messages": [],
    "stream": False
}

while True:

    prompt = input("Enter your prompt: ").strip()

    if not prompt:
        continue

    if prompt == "exit":
        break

    json_body["messages"].append({"role" : "user", "content" : prompt})

    response = requests.post(
        url=url,
        json=json_body
    )

    if response.status_code == 200:
        assistant = response.json()["message"]["content"]
        json_body["messages"].append({"role" : "assistant", "content" : assistant})
        print("Response :", assistant)

    else:
        print(response.status_code, response.text)
        break