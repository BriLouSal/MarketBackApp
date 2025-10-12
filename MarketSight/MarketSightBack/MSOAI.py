import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
open_ai_key = os.getenv("OPENAPI")
client = OpenAI(api_key=open_ai_key)