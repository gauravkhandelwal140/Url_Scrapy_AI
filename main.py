from fastapi import FastAPI, Header, HTTPException
from ai_v1 import extract_info, extract_info_with_question
from config import SECRET_API_KEY
from model import WebsiteInfo, WebsiteRequest, QARequest, QAResponse
from scraper import scrape_homepage
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def Index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/scrape_data", response_model=WebsiteInfo)
def analyze_website(data:WebsiteRequest,authorization: str = Header(None)):
    if authorization != f"Bearer {SECRET_API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    raw_text = scrape_homepage(url=data.url)
    if not raw_text:
        raise HTTPException(status_code=400, detail="Unable to extract website content")
    analysis = extract_info(raw_text)
    return WebsiteInfo(**analysis)


@app.post("/scrape_data_with_question", response_model=QAResponse)
def analyze_website(data: QARequest,authorization: str = Header(None)):
    if authorization != f"Bearer {SECRET_API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    raw_text = scrape_homepage(data.url)
    if not raw_text:
        raise HTTPException(status_code=400, detail="Unable to extract website content")
    analysis = extract_info_with_question(text=raw_text,question=data.question)

    # analysis={'question': 'Tell me compney name and company_size',
    #  'answer': {'company_name': 'Bombay Shaving Company', 'company_size': 'Founded in 2016'}}
    return QAResponse(**analysis)