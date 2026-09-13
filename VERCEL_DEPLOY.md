# WellCase — Vercel 24/7

This version is designed for **one Vercel project**:
- React is built from `frontend/`
- FastAPI is exposed at `/api/*` through `api/index.py`
- In production React automatically calls `/api`

## Required environment variables

Set in Vercel Project Settings → Environment Variables:

```text
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME
FRONTEND_URLS=https://YOUR-PROJECT.vercel.app
```

Do **not** use SQLite in production. Use Neon, Supabase, or another persistent PostgreSQL provider.

## Deploy

Import the repository/project with root `WellCase/`, then deploy.

After the first deployment, initialize the PostgreSQL schema/data using the project's production seed script from an environment where the database is reachable:

```bash
python backend/seed_production.py
```

## API

Production API base:
`/api`

Examples:
- `/api/auth/token`
- `/api/cases/`
- `/api/openings/1`
- `/api/inventory/`
- `/api/leaderboard/`


## Avatar / PP
The profile picture is resized client-side to 256x256 WebP and stored in the database as a data URL. This avoids relying on Vercel's ephemeral filesystem, so the PP remains available after redeploys when using a persistent PostgreSQL DATABASE_URL.

## New cases
The API runs a small catalog sync at startup and adds the Neon, Knife, Covert and Supreme cases to an existing database without duplicating them.
