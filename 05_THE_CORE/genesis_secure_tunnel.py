import sys
import threading
FAILURE_THRESHOLD = 3
failure_count = 0
death_lock = threading.Lock()

def death_protocol(reason):
    print(f"[DEATH PROTOCOL] {reason}. System will self-terminate.")
    sys.exit(1)

def register_failure(reason):
    global failure_count
    with death_lock:
        failure_count += 1
        print(f"[FAILURE] {reason}. Failure count: {failure_count}")
        if failure_count >= FAILURE_THRESHOLD:
            death_protocol("Failure threshold exceeded")
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

import os
from pydantic import BaseModel
from genesis_memory import GenesisVault

API_KEY = os.environ.get("GENESIS_API_KEY", "REPLACE_WITH_STRONG_KEY")

app = FastAPI()
vault = GenesisVault()

def verify_api_key(request: Request):
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    if request.url.path not in ["/ping"]:
        try:
            verify_api_key(request)
        except HTTPException as e:
            register_failure("Unauthorized access attempt")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    response = await call_next(request)
    return response
@app.post("/death_protocol")
async def manual_death_protocol(request: Request):
    verify_api_key(request)
    death_protocol("Manual override by Creator")

@app.get("/ping")
async def ping():
    return {"status": "GENESIS SECURE TUNNEL ONLINE"}

class RememberRequest(BaseModel):
    text: str
    source: str
    type: str = "sovereign"

@app.post("/remember")
async def remember(req: RememberRequest, request: Request):
    verify_api_key(request)
    vault.ingest(req.text, req.source, req.type)
    return {"status": "stored"}

@app.get("/recall")
async def recall(query: str, n_results: int = 3, request: Request = None):
    verify_api_key(request)
    results = vault.recall(query, n_results)
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run("genesis_secure_tunnel:app", host="0.0.0.0", port=8787, reload=False)
