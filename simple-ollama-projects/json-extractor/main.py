import  ollama

MODEL = "llama3.2"

user_text = input("Enter your text: ")

prompt = f"""
You are a data extraction system. 
Extract the following information from the user's text:

{user_text}

name
age
city
occupation

Return the result only as valid JSON using exactly these keys:

name, age, city, occupation

If a value cannot be found in the text, use null.

Do not add explanations, markdown, or any text outside the JSON object.
"""

response = ollama.generate(
    model=MODEL,
    prompt=prompt,
    format="json"
)

print(response.response)
