# V67 — Arsenal cases removed

- Removed the five Arsenal case seeds from the backend catalogue synchronizer.
- Any existing case whose name contains `Arsenal` is automatically deactivated during catalogue sync, so it disappears from the public catalogue even on an existing database.
- Legacy `Knife Case` / `Solid Knife Case` remain hidden.
- Added a frontend defensive filter so Arsenal cases cannot be rendered even if an old API response is cached.
- Removed Arsenal-specific rendering from the active case visual, preview modal, case detail page, and opening splash.
- The regular WellCase case-opening splash remains for the remaining cases.
- Existing historical openings are not deleted; only the retired cases are hidden/unopenable.
