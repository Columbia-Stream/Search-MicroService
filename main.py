# source venv/bin/activate

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from resources.search_resource import router as search_router

# Initialize FastAPI app
app = FastAPI(title="Search Service", version="0.1.0")

# 3️Allow frontend (React) to call FastAPI (CORS setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins for now (safe for local dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple root route
@app.get("/")
def root():
    return {"message": "Search Service is running"}

# Register all routes (under /api prefix)
app.include_router(search_router, prefix="/api")
