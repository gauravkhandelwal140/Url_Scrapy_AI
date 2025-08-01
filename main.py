from fastapi import FastAPI, Header, HTTPException
from langchain_community.vectorstores import FAISS

from ai_v1 import extract_info, extract_info_with_question, get_ai_answer
from config.config import SECRET_API_KEY
from healper.healper import scrape_url, clean_and_chunk, embadding_chunk_data, store_embeddings, is_already_embedded, \
    url_to_namespace, get_context_from_vactordb

from model import WebsiteInfo, WebsiteRequest, QARequest, QAResponse
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from middlewares import AuthMiddleware

app = FastAPI()
app.add_middleware(AuthMiddleware)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def Index(request: Request):
    return templates.TemplateResponse("index_v1.html", {"request": request})

@app.post("/process_url")
def process_url(data:WebsiteRequest):
    print('scrap_data')
    url=data.url
    if is_already_embedded(url=url):
        return {"status": "completed", "message": " already ChatBot created"}

    raw_text = scrape_url(url=url)
    clean_chunk_data=clean_and_chunk(raw_text)
    embadding_data=embadding_chunk_data(clean_chunk_data)
    store_embeddings(url,clean_chunk_data,embadding_data)
    return {"status": "completed", "message": "ChatBot created"}

@app.post("/chatbot_question")
async def chatbot_question(data: dict):
    url = data.get("url")
    question = data.get("question")
    namespace = url_to_namespace(str(url))
    if not is_already_embedded(url):
        return {"error": "This URL is not processed yet. Please start the app first."}
    context=get_context_from_vactordb(namespace,question)
    response=get_ai_answer(context, question)
    return {"answer": response.answer}

@app.post("/scrape_data", response_model=WebsiteInfo)
def analyze_website(data:WebsiteRequest):
    raw_text = scrape_url(url=data.url)
    if not raw_text:
        raise HTTPException(status_code=400, detail="Unable to extract website content")
    analysis = extract_info(raw_text)
    return WebsiteInfo(**analysis)

@app.post("/scrape_data_with_question", response_model=QAResponse)
def analyze_website(data: QARequest):
    raw_text = scrape_url(data.url)
    if not raw_text:
        raise HTTPException(status_code=400, detail="Unable to extract website content")
    analysis = extract_info_with_question(text=raw_text,question=data.question)
    return QAResponse(**analysis)