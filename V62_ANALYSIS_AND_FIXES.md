# V62 analysis and fixes

## Problems found
1. `CaseDetailPage` used only `resolveCaseImage()`. Arsenal cases intentionally have no legacy static case image mapping, so their detail page fell back to the placeholder.
2. `CaseOpeningSplashUnified` imported `isArsenalCase` but never used it. It rendered the CSS-generated crate for every case, so normal cases lost their real case artwork during the opening splash.
3. `GET /cases/preview/{case_id}` did not run the catalog synchronization used by `GET /cases/`. A direct preview could therefore return 404/stale catalog data on a database that had not yet been reconciled.
4. The frontend production build could not be rebuilt in this sandbox because `node_modules` is absent; `npm ci` did not complete within the available execution window. Python sources do pass `compileall`.

## Changes applied
- Arsenal case detail pages now use the canonical `CaseVisual` renderer.
- The unified opening splash now uses `CaseVisual` only for Arsenal cases and the resolved real case image for standard cases.
- Added responsive sizing/glow for standard case artwork in the splash.
- Direct case preview now synchronizes the catalog before lookup, matching the main catalog endpoint.
- Removed an unused `CaseOpeningSplash` import from `CaseDetailPage`.

## Validation
- `python -m compileall -q backend api` passes.
- Local frontend build was not executable because `react-scripts` is not installed in the extracted environment. The project `package.json`/lockfile remain unchanged.
