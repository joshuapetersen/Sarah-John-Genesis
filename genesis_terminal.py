import subprocess
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os

API_KEY = os.environ.get("GENESIS_API_KEY", "REPLACE_WITH_STRONG_KEY")

app = FastAPI()

def verify_api_key(request: Request):
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/terminal")
async def run_terminal(request: Request):
    verify_api_key(request)
    data = await request.json()
    cmd = data.get("cmd")
    if not cmd:
        return JSONResponse(status_code=400, content={"error": "No command provided."})
    # Block media player and media file execution
    forbidden = ["wmplayer", "vlc", "wmp", ".mp3", ".mp4", ".avi", ".wav", ".mov", ".mkv", "media player", "video", "audio", "startfile"]
    if any(f in cmd.lower() for f in forbidden):
        return JSONResponse(status_code=403, content={"error": "Media player and media file execution is blocked by system policy."})
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("genesis_terminal:app", host="127.0.0.1", port=8765, reload=True)
