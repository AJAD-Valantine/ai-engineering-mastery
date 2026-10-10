from pathlib import Path

import requests

pdf_path = Path(
    r"C:\Users\HP\OneDrive\Documents\Repos\ai-engineering-mastery\rag-from-scratch\02\data\Human_Nutrition.pdf"
)

if not pdf_path.exists():
    print("File doesn't exist. Downloading...")
    download_link = (
        "https://pressbooks.oer.hawaii.edu/humannutrition2/open/download?type=print_pdf"
    )

    response: requests.Response = requests.get(download_link)

    if response.status_code == 200:
        pdf_path.parent.mkdir(parents=True, exist_ok=True)

        with open(pdf_path, "wb") as file:
            file.write(response.content)
        print(f"File downloaded and saved at {pdf_path}")
        print("Document Ingestion Done.")

    else:
        print(f"Download failed. Status code {response.status_code}")
else:
    print(f"File {pdf_path.name} exists.")
    print("Document Ingestion Done.")
