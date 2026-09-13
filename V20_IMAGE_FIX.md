# WellCase V20 — case image fix

The four added cases now use webpack-imported PNG assets from `frontend/src/assets/cases/`.
This makes the images part of the React production bundle and avoids failures caused by stale
database image_url values, public-path routing, or Vercel static asset routing.

Added:
- Neon Case
- Knife Case
- Covert Case
- Supreme Case

CaseCard prioritizes the bundled asset for these exact case names, then falls back to the API
image_url for all other cases.

The backend catalog sync still writes the canonical `/images/cases/*.png` paths and creates
the new cases if they are missing.
