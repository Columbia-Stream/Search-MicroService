
'''
from fastapi import APIRouter, Query, Header, HTTPException
from services.search_service import search_videos

router = APIRouter()

@router.get("/search/videos")
def search_videos_route(
    q: str = Query(None),
    course_id: str = Query(None),
    prof: str = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    authorization: str = Header(None)
):
    """
    Atomic Search microservice endpoint.
    Token verification handled upstream by Composite.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Future: verify token locally if required
    return search_videos(q, course_id, prof, limit, offset)

'''

# resources/search_resource.py
from fastapi import APIRouter, Query, Header, HTTPException
from services.search_service import search_videos

router = APIRouter()

@router.get("/search/videos")
def search_videos_route(
    q: str = Query(None),
    course_id: str = Query(None),
    prof: str = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    authorization: str = Header(None)
):
    """
    Search microservice delegates DB logic to Videos Composite Microservice.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    return search_videos(q, course_id, prof, limit, offset, authorization)
