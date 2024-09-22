from fastapi import FastAPI
from . import db
import os
from . import password
from fastapi import FastAPI, WebSocket
import uvicorn
from typing import AsyncGenerator, NoReturn
from .chatbot import Chatbot


cbot = Chatbot("ccr")

os.environ['OPENAI_API_KEY'] = password.OPENAI_API_KEY

async def get_ai_response(message: str) -> AsyncGenerator[str, None]:
    response = cbot.query(message)

    all_content = ""
    async for chunk in response:
        if hasattr(chunk, 'choices') and chunk.choices:
            content = chunk.choices[0].delta.content
            if content:
                all_content += content
                yield all_content
        else:
            # If the chunk doesn't have the expected structure, yield it as is
            yield str(chunk)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/legislation/{region}")
def read_legislation(region: str):
    database = db.DB()
    return database.get_legislationsByRegion(region)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> NoReturn:
    """
    Websocket for AI responses
    """
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        async for text in get_ai_response(message):
            await websocket.send_text(text)
