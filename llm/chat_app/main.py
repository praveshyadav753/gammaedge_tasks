from fastapi import FastAPI
from fastapi.templating import  Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
import uuid
import json
import os
from google import genai
from dotenv import load_dotenv
from chat_model import get_model

load_dotenv()

app = FastAPI()

api_key = os.getenv('GEN_AI')

client = genai.Client(api_key=api_key)

app.mount('/static',StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory='templates')

active_connections = []

@app.get('/',response_class=HTMLResponse)
async def get_chat(request:Request):
    user_id = str(uuid.uuid4())
    return templates.TemplateResponse("chat.html",{"request": request ,"user_id":user_id})
    
@app.websocket("/ws/{user_id}")
async def start_websocket(websocket:WebSocket,user_id:str):
    await websocket.accept()
    active_connections[user_id] = WebSocket

    try:
        while True:
            data = websocket.receive_text()
            message = json.loads(data)["message"]

            llm_res = await get_response(message)

            if llm_res:
                # await websocket.send_text() 
                await websocket.send_text(json.dumps({"response": llm_res}))
            else:
                llm_res= ""
                websocket.send_text(llm_res)    
    except WebSocketDisconnect :
                active_connections.pop(user_id, None)

