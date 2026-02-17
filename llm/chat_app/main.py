from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
import uuid
import json
import os
from google import genai
from dotenv import load_dotenv
from chat_model import get_response

load_dotenv()

app = FastAPI()

api_key = os.getenv("GEN_AI")

client = genai.Client(api_key=api_key)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")

active_connections = {}


@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    user_id = str(uuid.uuid4())
    return templates.TemplateResponse(
        "chat.html", {"request": request, "user_id": user_id}
    )


@app.websocket("/ws/{user_id}")
async def start_websocket(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_connections[user_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                message = payload.get("message", "")
            except json.JSONDecodeError:
                await websocket.send_text("Invalid message format")
                continue

            async for chunk in get_response(message):
                await websocket.send_text(  chunk)

          
    except WebSocketDisconnect:
        active_connections.pop(user_id, None)
        print(f"User {user_id} disconnected")
