from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openrouter import OpenRouter
from database import add_message, get_history
from config import OPENROUTER_API_KEY, IMA_SYSTEM_PROMPT

app = FastAPI()
openrouter = OpenRouter(api_key=OPENROUTER_API_KEY)

class ChatRequest(BaseModel):
    session_id: str  # Unique ID for this conversation
    message: str  # Just the new user message

@app.post("/chat")
def chat(request: ChatRequest):
    # 1. Save user message to database
    add_message(request.session_id, "user", request.message)

    # 2. Get full conversation history from database
    history = get_history(request.session_id)

    # 3. Build messages for AI (system prompt + history)
    messages = [{"role": "system", "content": IMA_SYSTEM_PROMPT}] + history

    # 4. Get AI response
    response = openrouter.chat.send(
        model="meta-llama/llama-3.3-70b-instruct:free",
        messages=messages
    )

    ai_message = response.choices[0].message.content

    # 5. Save AI response to database
    add_message(request.session_id, "assistant", ai_message)

    # 6. Return AI response to frontend
    return {"response": ai_message}

# Serve static files (HTML/CSS frontend)
app.mount("/", StaticFiles(directory="../static", html=True), name="static")
