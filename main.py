import os

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import ComfyUIController
import OllamaArtist

app = FastAPI()
# Allow requests from Vue (running on a different port, usually 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/ping")
def ping():
    return {"message": "Hello World"}

@app.get("/api/ping/systems")
def ping_systems():
    msg: str = ""
    if (ComfyUIController.ping() == False):
        raise HTTPException(
            status_code=500, detail="Error connecting to ComfyUI server"
        )
    if (OllamaArtist.ping() == False):
        raise HTTPException(
            status_code=500, detail="Error connecting to Ollama server"
        )
    return {"message": "Ollama and ComfyUI are up and running!"}


# Serve index.html for all other routes
@app.get("/{full_path:path}")
async def serve_vue(full_path: str):
    index_path = os.path.join("wwwroot", "index.html")
    return FileResponse(index_path)


app.mount("/", StaticFiles(directory="wwwroot", html=True), name="static")
