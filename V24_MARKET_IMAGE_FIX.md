# WellCase V24 — market publish + item image fix

- Market listing creation is atomic and returns a confirmed listing after DB flush/commit.
- Frontend no longer turns a post-publication refresh error into a false "publication failed" message.
- Newly added weapon skins now use browser-safe PNG assets bundled in React and mirrored in public/images/items.
- Backend catalog sync now writes PNG image paths for the new weapons.
- Resolver supports both old SVG and new PNG DB paths as a fallback.
