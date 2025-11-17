'''import requests
import os
from fastapi import HTTPException

VIDEOS_COMPOSITE_URL = os.getenv("VIDEOS_COMPOSITE_URL", "http://127.0.0.1:8082")

def search_videos(q=None, course_id=None, prof=None, limit=20, offset=0, authorization=None):
    """
    Delegates video query to the Videos Composite Microservice.
    Handles pagination and query parameters.
    """
    try:
        params = {
            "q": q,
            "course_id": course_id,
            "prof": prof,
            "limit": limit,
            "offset": offset,
        }
        params = {k: v for k, v in params.items() if v is not None}

        headers = {"Authorization": authorization} if authorization else {}

        res = requests.get(
            f"{VIDEOS_COMPOSITE_URL}/videos",
            params=params,
            headers=headers,
            timeout=5
        )

        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=res.text)

        data = res.json()

        # Keep pagination and links structure consistent for Composite→Frontend
        return {
            "items": data.get("items", []),
            "page_size": data.get("page_size", limit),
            "offset": data.get("offset", offset),
            "links": data.get("links", []) + [
                {"rel": "self", "href": f"/search/videos?q={q or ''}&limit={limit}&offset={offset}"}
            ]
        }

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Videos composite timeout")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Videos composite unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search service error: {str(e)}")

def get_video_by_id(video_id: int, authorization: str):
    """
    Calls Videos Composite to fetch a single video.
    """
    headers = {"Authorization": authorization}

    res = requests.get(
        f"{VIDEOS_COMPOSITE_URL}/videos/{video_id}",
        headers=headers,
        timeout=5
    )

    if res.status_code == 404:
        return None
    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=res.text)

    return res.json()'''


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
        "href": f"/search/videos?q={q or ''}&course_id={course_id or ''}&prof={prof or ''}&limit={limit}&offset={offset}"
    })
    return data