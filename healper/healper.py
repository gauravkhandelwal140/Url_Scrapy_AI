import os

import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.config import GOOGLE_API_KEY
import hashlib

from langchain.vectorstores import FAISS

embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

def scrape_url(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        return ""


def clean_and_chunk(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_text(text)


def embadding_chunk_data(doc:str):
    em_vactor=embedding.embed_documents(doc)
    return em_vactor


def url_to_namespace(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()

def is_already_embedded(url: str) -> bool:
    namespace = url_to_namespace(str(url))
    return os.path.exists(f"indexes/{namespace}/index.faiss")


def store_embeddings(url: str, chunks: list, vectors: list):
    faiss_index = FAISS.from_texts(chunks, embedding)
    faiss_index.save_local(f"indexes/{url_to_namespace(str(url))}")

def get_context_from_vactordb(namespace,question):
    db = FAISS.load_local(f"indexes/{namespace}", embedding, allow_dangerous_deserialization=True)
    # docs_and_scores = db.similarity_search_with_score(question, k=150)
    docs_and_scores = list(db.docstore._dict.values())
    combined_text = "\n".join([doc.page_content for doc in docs_and_scores])
    print(combined_text)
    return combined_text