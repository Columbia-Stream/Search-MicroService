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
    authorization: str = Header(None),
    if_none_match: str = Header(None)
):
    """
    Search endpoint with ETag support.
    Delegates to search_service.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    return search_videos(
        q=q,
        course_id=course_id,
        prof=prof,
        limit=limit,
        offset=offset,
        authorization=authorization,
        if_none_match=if_none_match
    )

'''from fastapi import APIRouter, Query, Header, HTTPException
from fastapi import Response
from services.search_service import (
    search_videos,
    get_video_by_id,
)

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

@router.get("/search/videos/{video_id}")
def get_video_by_id_route(
    video_id: int,
    authorization: str = Header(None),
    if_none_match: str = Header(None),
    response: Response = None,
):
    """
    GET single video with ETag validation.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    video = get_video_by_id(video_id, authorization)

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    etag = f"W/{hash(str(video))}"

    if if_none_match == etag:
        response.status_code = 304
        return None

    response.headers["ETag"] = etag
    return video
'''
