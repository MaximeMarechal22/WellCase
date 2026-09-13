# V68 — remove Arsenal compile error

- Removed the stale named `isArsenalCase` import from `CaseCard.js`.
- Arsenal cases remain retired/deactivated by backend catalog sync.
- Frontend case list continues to filter Arsenal names defensively.
- Removed stale `frontend/build` so Docker deployment cannot serve an old React bundle.
