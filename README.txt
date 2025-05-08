# Url_Scrapy_AI

Url_Scrapy_AI is a Python-based web scraping tool designed to extract and process content from URLs. and give realtime questions answer.
Installation
Clone the Repository:
git clone https://github.com/gauravkhandelwal140/Url_Scrapy_AI.git
cd Url_Scrapy_AI
Create a Virtual Environment (Optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:
pip install -r requirements.txt
Usage

Configure Settings:
Edit the config.py file to set your:
2 keys from your enverment or directly config.py file 
SECRET_API_KEY :this key is for api authorization 
GOOGLE_API_KEY : add google gemini api key

Run the fastapi server 
command:- fastapi dev main.py

Project Structure
Url_Scrapy_AI/
├── ai_v1.py        # AI model implementation
├── config.py       # Configuration settings
├── main.py         # Main execution script
├── model.py        # Data models and structures
├── scraper.py      # Web scraping logic
├── requirements.txt# Project dependencies
└── README.md       # Project documentation

Technology Used:
python
FastApi
Pydantic
Langchain
Google Gemini AI Model
BeautifulSoup 
requests
html
Bootstrap
Api doc:

https://url-scrapy-ai.onrender.com/scrape_data


live api- :
 1. 
    url:https://url-scrapy-ai.onrender.com/scrape_data  Note: this api give perdifined question  answer like  company_name,industry
    method:post
    header:{
      'Authorization': 'Bearer get_my_key'
    }
    data:{
        "url":"https://www.example.com/"
      }
    response:{
      "company_name": "xyz",
      "industry": "Men's Grooming",
      "company_size": null,
      "location": "India"
  }

2.
  url:https://url-scrapy-ai.onrender.com/scrape_data_with_question  Note: this api give runtime question  answer like  company_name,industry
    method:post
    header:{
      'Authorization': 'Bearer get_my_key'
    }
    data:{
       "url":"https://firmable.com/",
       "question": "Tell me compney name and company_size and compney locations "
    }
    response:{
    "question": "Tell me compney name and company_size and compney locations",
    "answer": {
        "company_name": "Firmable Solutions",
        "company_size": "Small or big business? We’ve got you covered. Our easy-to-use platform lets you get started in minutes, with flexible pricing to suit businesses of all sizes.",
        "company_locations": "Australia and New Zealand"
    }
}

Note: for local use change this  'url-scrapy-ai.onrender.com' to localhost or local ip-address

I have made a simple UI app
link: https://url-scrapy-ai.onrender.com/

