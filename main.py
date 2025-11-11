from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from resources.search_resource import router as search_router
from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Search Service", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router)

@app.get("/")
def root():
    return {"message": "Search Service is running"}

@app.get("/healthz")
def health():
    return {"ok": True}

