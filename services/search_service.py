import requests
import os
from fastapi import HTTPException

# Default to local DBService
DBSERVICE_URL = os.getenv("DBSERVICE_URL", "http://127.0.0.1:8081")

def search_videos(q=None, course_id=None, prof=None, limit=20, authorization=None):
    """
    Sends the search query and auth header to DBService.
    DBService handles token verification + MySQL querying.
    """
    params = {"q": q, "course_id": course_id, "prof": prof, "limit": limit}
    headers = {"Authorization": authorization}

    try:
        res = requests.get(
            f"{DBSERVICE_URL}/videos/search",
            params=params,
            headers=headers,
            timeout=5
        )

        # Handle non-200 responses from DBService
        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=res.text)

        return res.json()

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="DBService timeout")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="DBService unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search service error: {str(e)}")
