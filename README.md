# Search Microservice

## Overview

This microservice is responsible for search and retrieval of video metadata in our lecture platform. It exposes CRUD-style endpoints (GET/POST/PUT/DELETE) plus a health check, though most endpoints are currently stubbed.

### Features implemented so far

- `GET /search` → returns mock video data (in-memory) filtered by query parameters (`q`, `course_id`, `prof`)  
- CRUD stubs:
  - `POST /search` → returns `{ "detail": "Not implemented" }`  
  - `PUT /search/{video_id}` → returns `{ "detail": "Not implemented for video_id X" }`  
  - `DELETE /search/{video_id}` → returns `{ "detail": "Not implemented for video_id X" }`  
- `GET /healthz` → returns `{ "ok": true }`  
- Pydantic `Video` model to define response schema  
- Stubbed authentication (in `utils/auth.py`) via `verify_token` — returns a fake user, so endpoints work locally without real auth  
- Automatically generated OpenAPI / Swagger docs at `/docs`  
- Basic pytest tests (health + GET + stub methods) to validate endpoint responses  

---

## Assumptions & Design Decisions

- Until the real authentication (Zeal) is available, `verify_token` is a stub that returns a dummy user. Once Zeal is ready, this will be replaced with real JWT validation.  
- The CRUD stubs (POST, PUT, DELETE) are placeholders only. They do **not** modify any state. They exist so the API surface matches professor’s requirement of full CRUD.  
- The `GET /search` uses in-memory mock data (`MOCK_VIDEOS`) defined in `services/search_service.py`. This will later be replaced by queries to a video metadata database.  
- The `Video` model defines the data shape you can expect (fields like `video_id`, `title`, `course_id`, `prof_name`, `uploaded_at`, `gcs_path`) so that future integration and clients know what to expect.  
- All endpoints are synchronous (no async DB or external dependencies) for simplicity at this stage.  
- For the tests to work, the project root must be in `PYTHONPATH` so that `main.py` is importable (or tests should be run with `PYTHONPATH=. pytest`).  
- Testing is focused on verifying correct response shapes and status codes for the stubbed methods. No real data or database integration yet.  

---

## Getting Started (Development)

### Prerequisites

- Python 3.10+ (tested on Python 3.12)  
- `venv` (or another virtual environment method)  

### Setup 

```bash
# From project root
python3 -m venv venv
source venv/bin/activate            # macOS/Linux
# venv\Scripts\activate            # Windows (PowerShell)

pip freeze > requirements.txt
```

### Running the service
```bash 
uvicorn main:app --reload --port 8000
```

- Visit http://127.0.0.1:8000/healthz → {"ok": true}
- Visit http://127.0.0.1:8000/docs → Swagger UI where you can test GET /search, POST/PUT/DELETE stubs
- Use Try it out in Swagger to call endpoints
- GET /search?q=Kubernetes should return a mock video matching “Kubernetes Basics”

### Running Tests
```bash 
# Be sure project root is in PYTHONPATH, or run with
PYTHONPATH=. pytest -v
```

Tests cover:
- Health check endpoint
- GET /search (with and without query)
- POST /search
- PUT /search/{video_id}
- DELETE /search/{video_id}

### Next Steps (Future Integration)
- Replace the stub verify_token with real JWT validation connected to the Auth microservice (Zeal).
- Enforce role-based authorization in endpoints (e.g. students only allowed to search / read, faculty allowed to upload/edit/delete).
- Replace the in-memory mock dataset with database queries to a real video metadata store (PostgreSQL, etc.).
- Add advanced search capabilities: full-text search, filtering (by course, professor), pagination, fuzzy/autocomplete matching.
- Design and document more detailed API behavior (error codes, validation rules, input schemas, optional fields).
- UI creation and integration — build frontend pages (search page, listing, filters, playback) that consume your microservice endpoints.
- Improve the test suite: cover error responses, boundary cases, invalid inputs, integration tests (frontend ↔ search service).
- Add error handling, structured logging, metrics (latencies, error rates) to make the service production-ready.
- Add CI/CD pipeline (e.g. GitHub Actions), containerize the service with Docker (or other), and enable deployment to cloud environments (GCP, AWS, etc.).

### API Summary
| Method | Path                 | Description          | Returns / Behavior                                  |
|--------|----------------------|----------------------|-----------------------------------------------------|
| GET    | `/search`            | Search videos (mock) | List of `Video` objects                             |
| POST   | `/search`            | Create (stub)        | `{ "detail": "Not implemented" }`                   |
| PUT    | `/search/{video_id}` | Update (stub)        | `{ "detail": "Not implemented for video_id X" }`    |
| DELETE | `/search/{video_id}` | Delete (stub)        | `{ "detail": "Not implemented for video_id X" }`    |
| GET    | `/healthz`            | Health check         | `{ "ok": true }`                                     |
