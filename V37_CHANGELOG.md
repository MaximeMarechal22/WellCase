# V37 — Arsenal splash hard fix

- Fixed the root cause of Rifle/Knife/Gloves Arsenal splash placeholders.
- The splash resolver now uses the dedicated `arsenal_splash_*` React assets first.
- Added aliases for common production DB naming variants and legacy image URLs.
- If an old DB still stores `type_rifles/type_knives/type_gloves`, the splash still resolves to the dedicated splash asset, not the card asset.
- Existing case images and database are preserved.
