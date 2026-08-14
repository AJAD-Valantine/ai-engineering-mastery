import ollama
from pathlib import Path

input_file = Path(r"C:\Users\HP\OneDrive\Documents\Repos\ai-engineering-mastery\simple-ollama-projects\item-classifier\raw_data.txt")
output_file = Path(r"C:\Users\HP\OneDrive\Documents\Repos\ai-engineering-mastery\simple-ollama-projects\item-classifier\classified_data.txt")

if not input_file.exists():
    print("Input file does not exist")
    exit()

content = input_file.read_text()

while True:
    categories = input("Enter categories (separated with a ','): ")

    if categories:
        break

prompt = f"""
Classify these items 
{content}

for the given categories 
{categories}

if any item does not belong to a category, 
create a category and put it under that created category.
"""

MODEL = "llama3.2"

messages = [
    {"role" : "user", "content" : prompt}
]

response = ollama.generate(
    model=MODEL,
    prompt=prompt,
)

output_file.write_text(response.response)