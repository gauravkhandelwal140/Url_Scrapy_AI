import os

import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.config import GOOGLE_API_KEY,pinecode_db
import hashlib
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

os.environ["PINECONE_API_KEY"] = pinecode_db
pc = Pinecone(api_key=pinecode_db)

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
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
    return splitter.create_documents([text])


def embadding_chunk_data(doc:str):
    em_vactor=embedding.embed_documents(doc)
    return em_vactor


def url_to_namespace(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()

def is_already_embedded(url: str) -> bool:
    index_name = url_to_namespace(str(url))
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
    return index_name in existing_indexes


# def store_embeddings(url: str, chunks: list, vectors: list):
#     faiss_index = FAISS.from_texts(chunks, embedding)
#     faiss_index.save_local(f"indexes/{url_to_namespace(str(url))}")
#

# def get_context_from_vactordb(namespace,question):
#     db = FAISS.load_local(f"indexes/{namespace}", embedding, allow_dangerous_deserialization=True)
#     # docs_and_scores = db.similarity_search_with_score(question, k=150)
#     docs_and_scores = list(db.docstore._dict.values())
#     combined_text = "\n".join([doc.page_content for doc in docs_and_scores])
#     print(combined_text)
#     return combined_text

def store_embeddings(url: str, chunks: list, embedding_data=None):
    index_name = url_to_namespace(str(url))
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            deletion_protection="enabled",  # Defaults to "disabled"
        )

    index = pc.Index(index_name)
    vector_store = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embedding,
        index_name=index_name,
        namespace=index_name,
        pinecone_api_key=pinecode_db,
    )
    print(f"Stored {len(chunks)} chunks in Pinecone index: {index_name}")

def get_context_from_vectordb(namespace: str, question: str):
    # Connect to vectorstore using PineconeVectorStore
    print(namespace)
    vectorstore = PineconeVectorStore(
        index_name=namespace,
        embedding=embedding,
        namespace=namespace,
        pinecone_api_key=pinecode_db
    )
    docs = vectorstore.similarity_search(question, k=15,namespace=namespace)
    print(docs)
    combined_text = "\n".join([doc.page_content for doc in docs])
    print(combined_text)
    return combined_text
