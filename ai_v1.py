import json
import re
from config import GOOGLE_API_KEY
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", google_api_key=GOOGLE_API_KEY)
tweet_prompt = PromptTemplate.from_template("""
    Given the following homepage content, extract:
    1. The industry the company operates in.
    2. The size of the company (small, medium, large) if mentioned.
    3. The location or headquarters of the company if stated.
    4. The Compnay Name  

    Homepage Content:
    {text}

    Respond in JSON format like:
    {{  "company_name":".....",
        "industry": "...",
        "company_size": "...",
        "location": "..."
    }}
    """)
tweet_chain = LLMChain(llm=llm, prompt=tweet_prompt, verbose=True)

def extract_info(text: str) -> dict:
    resp = tweet_chain.invoke(input=text)
    clean_json_str = re.sub(r"```json|```", "", resp['text']).strip()
    # Step 2: Convert to dictionary
    parsed_data = json.loads(clean_json_str)
    return parsed_data



