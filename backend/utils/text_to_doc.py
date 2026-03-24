# utils/text_to_doc.py


import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from utils.web_crawler import fetch_wordpress_data



def merge_hyphenated_words(text):
    return re.sub(r"(\w)-\n(\w)", r"\1\2", text)


def fix_newlines(text):
    return re.sub(r"(?<!\n)\n(?!\n)", " ", text)


def remove_multiple_newlines(text):
    return re.sub(r"\n{2,}", "\n", text)

def normalize_spaces(text):
    return re.sub(r"\s+", " ", text)

def clean_text(text):
    functions = [
        merge_hyphenated_words,
        fix_newlines,
        remove_multiple_newlines,
        normalize_spaces
    ]

    for func in functions:
        text = func(text)

    return text


def text_to_docs(text, metadata):
    doc_chunks = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_text(text)

    for i, chunk in enumerate(chunks):
        enriched_metadata = metadata.copy()
        enriched_metadata["chunk_id"] = i

        doc = Document(
            page_content=chunk,
            metadata={
                "title": metadata.get("title", ""),
                "url": metadata.get("url", ""),   
                "type": metadata.get("type", ""),
                "chunk_id": i
            }
        )

        doc_chunks.append(doc)

    return doc_chunks


def get_doc_chunks(text, metadata):
    cleaned = clean_text(text)
    return text_to_docs(cleaned, metadata)


def process_all_documents(data):
    all_chunks = []

    for text, metadata in data:
        chunks = get_doc_chunks(text, metadata)
        all_chunks.extend(chunks)

    return all_chunks
