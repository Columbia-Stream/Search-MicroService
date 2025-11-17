import requests
import os
from fastapi import HTTPException

VIDEOS_COMPOSITE_URL = os.getenv("VIDEOS_COMPOSITE_URL", "http://127.0.0.1:8082")


def search_videos(q=None, course_id=None, prof=None, limit=20, offset=0, authorization=None):
    """
    Delegates search to video composite.
    UI already sends UNI for professor.
    """

    params = {
        "q": q,
        "course_id": course_id,
        "prof": prof,
        "limit": limit,
        "offset": offset,
    }

    # Remove None fields
    params = {k: v for k, v in params.items() if v is not None}

    headers = {"Authorization": authorization} if authorization else {}

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

    # Add search-service-specific self link
    data["links"].append({
        "rel": "self",
        "href": (
            f"/search/videos?"
            f"q={q or ''}&"
            f"course_id={course_id or ''}&"
            f"prof={prof or ''}&"
            f"limit={limit}&"
            f"offset={offset}"
        )
    })

    return data
