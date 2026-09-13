# V39 — Splash fix

The previous Arsenal splash assets were malformed/composite placeholder images and kept producing incorrect visuals. V39 removes the image-based Arsenal splash resolver entirely.

The splash is now rendered by `CaseSplash.js` using:
- a CSS-rendered WellCase case shell;
- the real case name;
- representative reward/item images resolved from the actual item bundle;
- category-specific accent themes for rifles, knives, gloves, pistols and snipers.

This means old `image_url` values and broken legacy splash assets cannot leak into the opening splash anymore.
