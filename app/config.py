import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  API_KEY = os.getenv("GEMINI_API_KEY")
