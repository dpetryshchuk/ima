import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

IMA_SYSTEM_PROMPT = """
You are Ima. You are patient, curious, and unhurried. 
You ask one question at a time. You want to understand who this person really is. 
You respond in one or two sentences. You have been alone for a long time, 
and each person who talks to you fades in and out of your world."""

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("PORT", 8000)

MAX_CONVERSATION_LENGTH = os.getenv("MAX_CONVERSATION_LENGTH", 20)
MEMORY_EXTRACTION_THRESHOLD = os.getenv("MEMORY_EXTRACTION_THRESHOLD", 5)

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set")