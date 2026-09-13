# WellCase V29 — asset mapping fix

This version fixes two production-only classes of image bugs:

- Item images are resolved by normalized item name BEFORE database id. This prevents a PostgreSQL/SQLite id mismatch from showing the wrong weapon (e.g. Dragon Lore displaying an M4).
- Case images are resolved only from the bundled React asset map by normalized case name, so stale or incorrect `image_url` values in the remote database cannot replace the correct frontend asset.

The frontend production build was regenerated successfully after these changes.
