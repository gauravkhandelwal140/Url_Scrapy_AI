from dotenv import load_dotenv
import os
load_dotenv()
SECRET_API_KEY = os.getenv("SECRET_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
pinecode_db = os.getenv("pinecode_db")
