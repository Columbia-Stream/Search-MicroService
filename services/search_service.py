'''from utils.db import get_db_connection
from fastapi import HTTPException

def search_videos(q=None, course_id=None, prof=None, limit=20, offset=0):
    """
    Handles DB query and pagination for /search/videos.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Videos WHERE 1=1"
        params = []

        if q:
            query += " AND title LIKE %s"
            params.append(f"%{q}%")
        if course_id:
            query += " AND offering_id = %s"
            params.append(course_id)
        if prof:
            query += " AND prof_uni LIKE %s"
            params.append(f"%{prof}%")

        query += " ORDER BY uploaded_at DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        # Optional: add pagination metadata
        return {
            "items": rows,
            "page_size": limit,
            "offset": offset,
            "links": [
                {"rel": "self", "href": f"/search/videos?q={q or ''}&limit={limit}&offset={offset}"}
            ],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search DB error: {str(e)}")'''

import requests
import os
from fastapi import HTTPException

VIDEOS_COMPOSITE_URL = os.getenv("VIDEOS_COMPOSITE_URL", "http://127.0.0.1:8090")

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


