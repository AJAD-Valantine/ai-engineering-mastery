import requests

url = "http://localhost:11434/api/chat"
MODEL = "llama3.2"

prompt = input("Enter your prompt: ").strip()

json_body = {
    "model": MODEL,
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "stream": False
}

response = requests.post(
    url=url,
    json=json_body
)

if response.status_code == 200:
    print(response.json()["message"]["content"])
else:
    print(response.status_code, response.text)