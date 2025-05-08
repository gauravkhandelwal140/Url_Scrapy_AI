import json
import re
from config import GOOGLE_API_KEY
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", google_api_key=GOOGLE_API_KEY)

def extract_info(text: str) -> dict:
    prompt = PromptTemplate.from_template("""
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
    tweet_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    resp = tweet_chain.invoke(input=text)
    clean_json_str = re.sub(r"```json|```", "", resp['text']).strip()
    # Step 2: Convert to dictionary
    parsed_data = json.loads(clean_json_str)
    return parsed_data


def extract_info_with_question(text: str,question:str):
    prompt = PromptTemplate.from_template("""
            You are an assistant helping extract business information from a website homepage.
        
            Homepage Content:
            \"\"\"{content}\"\"\"
        
            Question: {question}
            Ignore content in response    
            Answer in JSON format:
            {{ 
                "question": "<repeat the question>",
                "answer": "<your answer here>"
            }}
        """)
    tweet_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    resp = tweet_chain.invoke({"content": text,"question": question })
    clean_json_str = re.sub(r"```json|```", "", resp['text']).strip()
    # Step 2: Convert to dictionary
    parsed_data = json.loads(clean_json_str)
    print(parsed_data,'---------59')
    return parsed_data