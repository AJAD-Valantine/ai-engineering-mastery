from typing import Any

import pymupdf
from ingestion import pdf_path


def text_formatter(text: str) -> str:
    cleaned_text: str = text.replace("\n", " ").strip()
    return cleaned_text


def open_and_read_pdf(path) -> list[dict]:

    doc: pymupdf.Document = pymupdf.open(path)
    pages: list[dict] = []

    for page_number, page in enumerate(doc, start=-41):  # type: ignore
        text = page.get_text()
        text: str = text_formatter(text)

        pages.append(
            {
                "page_number": page_number,
                "page_char_count": len(text),
                "page_word_count": len(text.split(" ")),
                "page_sentence_count_raw": len(text.split(". ")),
                "page_token_count": len(text) / 4,
                "text": text,
            }
        )
    return pages

page_data: list[dict[str, Any]] = open_and_read_pdf(pdf_path)
print("Document Pre-processing Done.")
