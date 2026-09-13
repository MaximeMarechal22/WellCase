# WellCase V7 — ouverture + Vercel

- Case opening now loads case data before charging/opening the case.
- Opening animation always has a fallback pool containing the server-selected winner, so it cannot remain stuck because the case contents array is empty.
- Opening requests have a 10s axios timeout and display the backend error instead of spinning forever.
- React Strict Mode remains protected against duplicate openings.
- Winner image paths are normalized and work on the same Vercel origin.
- Leaderboard is reset as a new season at `2026-09-13T01:21:40+00:00`; old opening/upgrade/reward history is preserved.
- Vercel is now configured as one project: CRA frontend + FastAPI under `/api`.
- Production PostgreSQL support added with `psycopg` and SQLite-only connection args fixed.
- Tables are created automatically; `backend/seed_production.py` seeds a fresh production database without demo credentials.
