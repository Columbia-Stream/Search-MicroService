from fastapi import APIRouter, Query, Header, HTTPException
from typing import List
from models.video import Video
from services.search_service import search_videos

router = APIRouter()

@router.get("/search", response_model=List[Video])
def search(
    q: str = Query(None),
    course_id: str = Query(None),
    prof: str = Query(None),
    limit: int = Query(20),
    authorization: str = Header(None)
):
    """
    Forward search request and Authorization header to DBService.
    The DBService handles token verification + DB queries.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    return search_videos(q, course_id, prof, limit, authorization)


@router.get("/healthz")
def healthz():
    """Health check endpoint"""
    return {"ok": True}
