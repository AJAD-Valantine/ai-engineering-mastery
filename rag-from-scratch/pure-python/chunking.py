import re

from pre_processing import page_data
from spacy.lang.en import English

nlp = English()
nlp.add_pipe("sentencizer")

for item in page_data:

    item["sentences"] = [
        str(sentence)
        for sentence in list(nlp(item["text"]).sents)
        ]
    item["sentence_count"] = len(item["sentences"])


def slice_list(input_list: list, slice_size: int = 10) -> list[list]:
    result = []
    for i in range(0, len(input_list), slice_size):
        result.append(input_list[i : i + slice_size])
    return result


for item in page_data:
    item["sentence_chunks"] = slice_list(item["sentences"], slice_size=10)

chunks = []

for item in page_data:

    for sentence_group in item["sentence_chunks"]:

        if item["page_number"] < 0:
            continue

        chunk_dict = {"page_number": item["page_number"]}

        joined_sentence_chunk = " ".join(sentence_group).replace("  ", " ").strip()
        joined_sentence_chunk = re.sub(
            pattern=r"\.([A-Z])",
            repl=r". \1",
            string=joined_sentence_chunk
        )

        chunk_dict["chunk"] = joined_sentence_chunk
        chunk_dict["chunk_char_count"] = len(joined_sentence_chunk)
        chunk_dict["chunk_word_count"] = len(joined_sentence_chunk.split(" "))
        chunk_dict["chunk_token_count"] = len(joined_sentence_chunk) / 4

        if chunk_dict["chunk_token_count"] < 30:
            continue

        chunks.append(chunk_dict)

print("Document Chunking Done.")
