import requests
import json

url = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

prompt = input("Enter your prompt: ").strip()

json_body = {
    "model" : MODEL,
    "prompt" : prompt,
    "stream" : True,
}

response = requests.post(
    url=url,
    json=json_body,
    stream=True
)

if response.status_code == 200:
    for line in response.iter_lines():
        line = line.decode("utf-8")
        chunk = json.loads(line)
        print(chunk["response"], flush=True, end="")

else:
    print(response.status_code, response.text)