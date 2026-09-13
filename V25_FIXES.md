# V25 fixes

- Removed the empty SMG/PM collection from the Collections page/backend because no SMG/PM items exist in the catalog.
- Added authoritative local asset overrides for new weapon skins and corrected AWP | Dragon Lore to use a real AWP asset instead of the stale M4 image.
- Regenerated local PNGs for the new skin set from known-good weapon silhouettes so name and weapon type cannot drift.
- Fixed daily reward UI so the claim card disappears immediately after claiming and stays hidden when the backend reports `can_claim=false`.
- Hardened daily reward date matching by comparing the stored claim date in Python, avoiding UTC/local midnight edge cases.
