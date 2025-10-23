from fastapi import Header, HTTPException
import requests
import os

# Default to local Auth service, but allow override via environment variable
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://127.0.0.1:8000/auth/verify-token")

def verify_token(authorization: str = Header(None)):
    """
    Verify Firebase ID token with the Auth microservice.

    - Expects Authorization: Bearer <id_token>
    - Calls /auth/verify-token endpoint of Auth microservice
    - Returns decoded user info (uid, email, role)
    """

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    try:
        # Send request to Auth microservice
        res = requests.get(AUTH_SERVICE_URL, headers={"Authorization": authorization}, timeout=5)

        # Handle non-200 responses
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code,
                detail=f"Auth verification failed: {res.text}"
            )

        # Extract verified token data
        data = res.json()

        # Return a simplified structure usable by other routes
        return {
            "uid": data.get("uid", "unknown"),
            "email": data.get("email", "unknown"),
            # simple role inference – you can refine later
            "role": "faculty" if data.get("email", "").endswith("@columbia.edu") else "student"
        }

    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Auth service timeout")
    except requests.ConnectionError:
        raise HTTPException(status_code=503, detail="Auth service unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auth verification error: {str(e)}")

