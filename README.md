FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.sherlock_service import run_sherlock
from services.holehe_service import run_holehe
from services.phoneinfoga_service import run_phoneinfoga
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/sherlock")
async def sherlock_endpoint(payload: dict):
    username = payload.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="username required")
    return await run_sherlock(username)

@app.post("/holehe")
async def holehe_endpoint(payload: dict):
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="email required")
    return await run_holehe(email)

@app.post("/phoneinfoga")
async def phoneinfoga_endpoint(payload: dict):
    phone = payload.get("phoneNumber")
    if not phone:
        raise HTTPException(status_code=400, detail="phoneNumber required")
    return await run_phoneinfoga(phone)

# Microservicio OSINT FastAPI

Despliegue rápido usando Sherlock, Holehe y PhoneInfoga.

## Instalación
pip install -r requirements.txt
uvicorn main:app --reload

fastapi
uvicorn
