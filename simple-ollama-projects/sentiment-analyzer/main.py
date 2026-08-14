import  ollama

MODEL = "llama3.2"

user_text = input("Enter your text: ")

prompt = f"""
You are a sentiment analysis system. 
Analyze the user's text and classify its sentiment.

{user_text}

The sentiment must be exactly one of:

positive
negative
neutral
mixed

Return these two values:
sentiment -
reason -

reason should be a short explanation of why the text was classified that way.
"""

response = ollama.generate(
    model=MODEL,
    prompt=prompt,
)

print(response.response)
