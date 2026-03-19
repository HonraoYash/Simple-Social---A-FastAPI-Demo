# FastAPI Social Backend Demo

This project is a **learning-focused FastAPI backend demo** built to show that I can design and implement a real backend service with authentication, database integration, and media workflows.

The frontend (Streamlit) is included for demonstration, but the primary goal of this project is to showcase backend development using **FastAPI**.

## Live Demo

- Frontend (Streamlit): [https://simple-social-fastapi-backend-demo.streamlit.app/](https://simple-social-fastapi-backend-demo.streamlit.app/)
- Backend API Docs (Fastapi, Vercel): [https://simple-social-a-fast-api-demo.vercel.app/docs](https://simple-social-a-fast-api-demo.vercel.app/docs)

## Project Purpose

- Learn and apply FastAPI fundamentals in a practical app.
- Build a production-style backend flow: auth, uploads, feed, and ownership checks.
- Demonstrate async database operations and clean API design.
- Integrate a third-party media service (ImageKit) from the backend.

## What This Backend Demonstrates

- **FastAPI app structure** with modular files (`app/app.py`, `app/db.py`, `app/users.py`).
- **JWT authentication** using `fastapi-users`.
- **User management** endpoints (register, login, profile, verification/reset routes).
- **Async SQLAlchemy + SQLite** persistence.
- **Media upload API** that stores files via ImageKit and metadata in DB.
- **Feed API** returning enriched post data.
- **Authorization checks** (only the owner can delete a post).

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy (async) + aiosqlite
- fastapi-users
- ImageKit SDK
- Streamlit (demo UI)

## API Endpoints (Key)

### Auth/User (via fastapi-users)

- `POST /auth/register`
- `POST /auth/jwt/login`
- `GET /users/me`
- Plus password reset + verification routes under `/auth/*`

### Custom Project Endpoints

- `POST /upload`  
  Upload image/video, store in ImageKit, save post in DB.
- `GET /feed`  
  Fetch posts in reverse-chronological order with owner/email metadata.
- `DELETE /posts/{post_id}`  
  Delete a post only if the authenticated user is the owner.

## Project Structure

```text
.
├── app/
│   ├── app.py        # FastAPI routes and app lifecycle
│   ├── db.py         # SQLAlchemy models + async session
│   ├── images.py     # ImageKit client setup
│   ├── schemas.py    # Pydantic/FastAPI-Users schemas
│   └── users.py      # Auth backend and user manager
├── frontend.py       # Streamlit demo client
├── main.py           # Uvicorn entrypoint
└── pyproject.toml    # Dependencies
```

## Setup

1. Clone the repo and move into the project directory.
2. Create a `.env` file with your ImageKit credentials:

```env
IMAGEKIT_PRIVATE_KEY=your_private_key
IMAGEKIT_PUBLIC_KEY=your_public_key
IMAGEKIT_URL=your_url_endpoint
```

3. Install dependencies:

```bash
uv sync
```

## Run the Project

### 1) Start FastAPI backend

```bash
uv run main.py
```

Backend runs on `http://localhost:8000`.

### 2) (Optional) Start demo frontend

```bash
uv run streamlit run frontend.py
```

Frontend runs on `http://localhost:8501`.

## Why This Project Matters

This project is my backend learning milestone for FastAPI.  
It proves I can:

- build authenticated APIs,
- model and query relational data asynchronously,
- integrate external services cleanly,
- and deliver an end-to-end working backend with real features.

