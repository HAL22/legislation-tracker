from fastapi import FastAPI
# from . import db
from . import db
import os
from fastapi import FastAPI, WebSocket
import uvicorn
from typing import AsyncGenerator, NoReturn
from . import chatbot
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

with open("src/FE/index.html") as f:
    html = f.read()

async def get_ai_response(cbot,message: str) -> AsyncGenerator[str, None]:
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    database = db.DB()
    database.initialize_database()
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="src/FE"), name="static")

@app.get("/")
async def web_app() -> HTMLResponse:
    """
    Web App
    """
    return HTMLResponse(html)

@app.get("/legislation/{region}")
async def read_legislation(region: str):
    database = db.DB()
    print(f"Accessing legislation for region: {region}")
    legislation = database.get_legislationsByRegion(region)
    print(f"Retrieved legislation: {legislation}")
    return legislation


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str) -> NoReturn:
    """
    Websocket for AI responses
    """
    cbot = chatbot.Chatbot(client_id)
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        async for text in get_ai_response(cbot,message):
            await websocket.send_text(text)

@app.get("/test")
async def test_endpoint():
    print("Test endpoint accessed")  # This will appear in your Fly.io logs
    return {"message": "Test endpoint working"}
