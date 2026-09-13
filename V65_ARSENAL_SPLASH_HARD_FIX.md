# V65 — Arsenal splash hard fix

- Arsenal splash no longer uses the API `image_url` or dynamically built paths.
- Each of the five Arsenal categories imports a local bundled artwork directly.
- Added `onError` fallback to `CaseVisual`.
- Splash case data is stored at click/open time, avoiding an ID/type lookup race.
- Splash visibility increased from 1.45s to 2.2s.
- The Dockerfile already rebuilds the CRA frontend from `frontend/src`, so the bundled assets are included during deployment.

CRA recommends importing assets from JS so webpack includes them in the production bundle and missing assets fail at compile time instead of becoming runtime 404s.
