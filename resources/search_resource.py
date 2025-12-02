from fastapi import APIRouter, Query, Header, HTTPException
from services.search_service import search_videos

router = APIRouter()

@router.get("/search/videos")
def search_videos_route(
    q: str = Query(None),
    course_id: str = Query(None),
    offering_id: int = Query(None),
    prof: str = Query(None),
    year: int = Query(None),           # NEW
    semester: str = Query(None),       # NEW
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    authorization: str = Header(None),
    if_none_match: str = Header(None)
):
    """
    Search endpoint with ETag + Authorization.
    """

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    return search_videos(
        q=q,
        course_id=course_id,
        offering_id=offering_id,
        prof=prof,
        year=year,               # NEW
        semester=semester,       # NEW
        limit=limit,
        offset=offset,
        authorization=authorization,
        if_none_match=if_none_match
    )
