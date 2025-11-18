# services/search_service.py
import requests
import os
import hashlib
import json
from fastapi import HTTPException, Response

VIDEOS_COMPOSITE_URL = os.getenv("VIDEOS_COMPOSITE_URL", "http://127.0.0.1:8082")


def search_videos(q=None, course_id=None, prof=None,
                  limit=20, offset=0,
                  authorization=None,
                  if_none_match=None):
    """
    Delegates search to Videos Composite Microservice.
    Implements ETag caching behavior.
    """

    # Build clean params list (remove None)
    params = {
        "q": q,
        "course_id": course_id,
        "prof": prof,
        "limit": limit,
        "offset": offset,
    }
    params = {k: v for k, v in params.items() if v is not None}

    headers = {"Authorization": authorization} if authorization else {}

    # ---- Call Video Composite ----
    try:
        res = requests.get(
            f"{VIDEOS_COMPOSITE_URL}/videos",
            params=params,
            headers=headers,
            timeout=5
        )
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Videos composite timeout")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Videos composite unavailable")

    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=res.text)

    data = res.json()

    # ---- Compute ETag using hash of items ----
    items_json = json.dumps(data.get("items", []), sort_keys=True).encode("utf-8")
    etag = hashlib.sha256(items_json).hexdigest()

    # ---- Handle conditional GET (If-None-Match) ----
    if if_none_match == etag:
        # Return 304 with no body
        return Response(status_code=304)

    # ---- Add Search MS self link ----
    data["links"].append({
        "rel": "self",
        "href": (
            f"/search/videos?"
            f"q={q or ''}&"
            f"course_id={course_id or ''}&"
            f"prof={prof or ''}&"
            f"limit={limit}&offset={offset}"
        )
    })

    # ---- Return response with ETag header ----
    response = Response(
        content=json.dumps(data),
        media_type="application/json"
    )
    response.headers["ETag"] = etag
    return response
