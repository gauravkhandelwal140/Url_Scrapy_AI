from __future__ import annotations
from pydantic import BaseModel, HttpUrl
from typing import Optional, Union


class WebsiteRequest(BaseModel):
    url: HttpUrl

class WebsiteInfo(BaseModel):
    company_name:Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    location: Optional[str] = None




class QARequest(BaseModel):
    url: HttpUrl
    question: str

class QAResponse(BaseModel):
    question: Optional[str] = None
    answer:  Optional[Union[str, dict]] = None
