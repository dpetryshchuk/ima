from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from openrouter import OpenRouter
from dotenv import load_dotenv
import os


load_dotenv()

app = FastAPI()
openrouter = OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY"))

@app.post("/chat")
def chat(message: str):
    response = openrouter.chat.send(
        model="meta-llama/llama-3.3-70b-instruct:free",
        messages=[
            {
                "role": "system",
                "content": "You are Ima. You are patient, curious, and unhurried. You ask one question at a time. You want to understand who this person really is. You respond in one or two sentences."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )
    return {"response": response.choices[0].message.content}
    
# This will show the static files, ima_app
app.mount("/", StaticFiles(directory="static", html=True), name="static")
