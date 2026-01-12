from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openrouter import OpenRouter
from database import add_message, get_history
from config import OPENROUTER_API_KEY, IMA_SYSTEM_PROMPT, BACKSTORY_SYSTEM_PROMPT

app = FastAPI()
openrouter = OpenRouter(api_key=OPENROUTER_API_KEY)

class ChatRequest(BaseModel):
    session_id: str  # Unique ID for this conversation
    message: str  # Just the new user message

class BackstoryRequest(BaseModel):
    text: str

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

@app.get("/history/{session_id}")
def history(session_id: str):
    return get_history(session_id)

@app.post("/parse-backstory")
def parse_backstory(request: BackstoryRequest):
    import json

    message = [{"role": "system", "content": BACKSTORY_SYSTEM_PROMPT}, {"role": "user", "content": request.text}]
    response = openrouter.chat.send(
        model="meta-llama/llama-3.3-70b-instruct:free",
        messages=message
    )

    # Extract JSON from response (between first { and last })
    raw_output = response.choices[0].message.content
    first_brace = raw_output.find('{')
    last_brace = raw_output.rfind('}')

    if first_brace != -1 and last_brace != -1:
        json_str = raw_output[first_brace:last_brace+1]
        parsed = json.loads(json_str)
        return parsed
    else:
        return {"error": "No JSON found in response", "raw": raw_output}


# Serve static files (HTML/CSS frontend)
app.mount("/", StaticFiles(directory="../static", html=True), name="static")
