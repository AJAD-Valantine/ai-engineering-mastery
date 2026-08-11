import requests

url = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

prompt = input("Enter your prompt: ").strip()

json_body = {
    "model": MODEL,
    "prompt": prompt,
    "stream": False
}

response = requests.post(
    url=url,
    json=json_body
)

if response.status_code == 200:
    print(response.json()["response"])
else:
    print(response.status_code, response.text)