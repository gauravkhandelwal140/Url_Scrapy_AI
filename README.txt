# Url_Scrapy_AI
Url_Scrapy_AI
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

api 

