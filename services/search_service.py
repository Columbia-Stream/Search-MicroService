import requests
import os
import hashlib
import json
from fastapi import HTTPException, Response

VIDEOS_COMPOSITE_URL = os.getenv("VIDEOS_COMPOSITE_URL", "http://34.44.10.169:8082")

def search_videos(
    q=None,
    course_id=None,
    offering_id=None,
    prof=None,
    year=None,              # NEW
    semester=None,          # NEW
    limit=20,
    offset=0,
    authorization=None,
    if_none_match=None
):
    """
    Delegates search to Videos Composite.
    Includes year + semester.
    """

    params = {
        "q": q,
        "course_id": course_id,
        "offering_id": offering_id,
        "prof": prof,
        "year": year,           # NEW
        "semester": semester,   # NEW
        "limit": limit,
        "offset": offset,
    }

    params = {k: v for k, v in params.items() if v is not None}

    headers = {"Authorization": authorization}

    # Call Composite
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

    # Compute ETag
    items_json = json.dumps(data.get("items", []), sort_keys=True).encode("utf-8")
    etag = hashlib.sha256(items_json).hexdigest()

    if if_none_match == etag:
        return Response(status_code=304)

    # Add HATEOAS link
    data["links"].append({
        "rel": "self",
        "href": (
            f"/search/videos?"
            f"q={q or ''}&"
            f"course_id={course_id or ''}&"
            f"offering_id={offering_id or ''}&"
            f"prof={prof or ''}&"
            f"year={year or ''}&"
            f"semester={semester or ''}&"
            f"limit={limit}&offset={offset}"
        )
    })

    response = Response(
        content=json.dumps(data),
        media_type="application/json"
    )
    response.headers["ETag"] = etag
    return response
