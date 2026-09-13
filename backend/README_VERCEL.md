# Vercel API

The Vercel project should use `backend/` as its Root Directory. `main.py` exposes the FastAPI `app` object while the existing `app/` package remains the source of the routes.

Set `DATABASE_URL` to a persistent PostgreSQL database in production. SQLite is for local development only.
