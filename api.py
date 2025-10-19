from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import ComfyUIController
import OllamaArtist

app = FastAPI()


@app.post("/api/ping")
def ping():
    msg: str = ""
    if(ComfyUIController.ping() == False):
        raise HTTPException(
            status_code=500, detail="Error connecting to ComfyUI server"
        )
    if(OllamaArtist.ping() == False):
        raise HTTPException(
            status_code=500, detail="Error connecting to Ollama server"
        )
    return {"message": "Ollama and ComfyUI are up and running!"}


app.mount("/", StaticFiles(directory="wwwroot", html=True), name="wwwroot")
