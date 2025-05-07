from fastapi import FastAPI, Header, HTTPException
from ai_v1 import extract_info
from config import SECRET_API_KEY
from model import WebsiteInfo, WebsiteRequest
from scraper import scrape_homepage

app = FastAPI()

@app.post("/scrape_data", response_model=WebsiteInfo)
def analyze_website(data: WebsiteRequest,authorization: str = Header(None)):
    if authorization != f"Bearer {SECRET_API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    raw_text = scrape_homepage(data.url)
    if not raw_text:
        raise HTTPException(status_code=400, detail="Unable to extract website content")

    analysis = extract_info(raw_text)
    return WebsiteInfo(**analysis)
