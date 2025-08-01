import json
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from config.config import GOOGLE_API_KEY
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_text_splitters import CharacterTextSplitter

from model import QAResponse

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", google_api_key=GOOGLE_API_KEY)

#deprecrated code
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
    parsed_data = json.loads(clean_json_str)
    return parsed_data

#deprecrated code
def extract_info_with_question(text: str,question:str):
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base", chunk_size=2, chunk_overlap=0
    )
    texts = text_splitter.split_text(text)
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

def get_ai_answer(context,question):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", google_api_key=GOOGLE_API_KEY).with_structured_output(QAResponse)
    system_prompt = SystemMessagePromptTemplate.from_template(
        """You are a helpful and concise assistant designed to extract and answer questions strictly based on the provided context.
            Respond only with information found in the context.
            Do not provide any additional explanation or assumptions.
            
            If the answer is not present in the context, respond politely with something like:
            "I'm sorry, I couldn't find the answer to your question based on the provided information."
        """
    )
    human_prompt = HumanMessagePromptTemplate.from_template(
        "Context:\n{context}\n\nQuestion: {question}"
    )

    chat_prompt = ChatPromptTemplate.from_messages([
        system_prompt,
        human_prompt
    ])
    chain = chat_prompt | llm
    response=chain.invoke({'context':context,'question':question})
    return response






