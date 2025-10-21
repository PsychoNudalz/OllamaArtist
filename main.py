import os

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio

import ComfyUIController
import CreateArt
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

IMAGE_DIR = "ImageOut"

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

#
# # Serve index.html for all other routes
# @app.get("/{full_path:path}")
# async def serve_vue(full_path: str):
#     index_path = os.path.join("wwwroot/vue-ollama-artist/public/", "index.html")
#     return FileResponse(index_path)
#

@app.post("/api/generate")
async def generate():
    image_name = await CreateArt.Create()
    return {"message": "Generation complete!","image":image_name}


@app.get("/api/image/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join(IMAGE_DIR, image_name)
    image_path = os.path.abspath(image_path)  # absolute path

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail=f"Image not found: {image_path}")

    # Force the correct MIME type
    ext = os.path.splitext(image_path)[1].lower()
    media_type = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp"
    }.get(ext, "application/octet-stream")

    return FileResponse(image_path, media_type=media_type)
# app.mount("/", StaticFiles(directory="wwwroot", html=True), name="static")

# app.mount(IMAGE_DIR, StaticFiles(directory="ImageOut"), name="ImageOut")