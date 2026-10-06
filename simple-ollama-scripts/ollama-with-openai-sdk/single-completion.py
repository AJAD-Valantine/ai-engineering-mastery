from openai import OpenAI

MODEL = "llama3.2"
url = "http://localhost:11434/v1"

client = OpenAI(
    base_url=url,
    api_key="ollama",
)

prompt = input("Enter your message: ")

response = client.completions.create(
    model=MODEL,
    prompt=prompt,
    temperature=0.3
)

print(response.choices[0].text)