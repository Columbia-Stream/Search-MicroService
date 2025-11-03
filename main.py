# source venv/bin/activate
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from resources.search_resource import router as search_router

# Initialize FastAPI app
app = FastAPI(title="Search Service", version="0.2.0")

# Allow frontend (React) to call FastAPI (CORS setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Relaxed for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Search Service running via DBService"}

# Register search routes
app.include_router(search_router, prefix="/api")
