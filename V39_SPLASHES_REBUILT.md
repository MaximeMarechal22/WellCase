# V39 — Splashes rebuilt from scratch

The previous Arsenal splash images were malformed composite images and were the source of the repeated placeholder/wrong-art bugs.

V39 does not use those splash-art image files for the opening splash anymore.

The opening splash is now a data-driven React component:
- CSS-rendered WellCase case shell;
- category-specific accent theme;
- real reward/item PNGs resolved by the existing item resolver;
- no dependency on DB `image_url` for Arsenal splash visuals;
- no dependency on the legacy `arsenal_splash_*` / `type_*` splash images.

This prevents an outdated asset from the database or an old placeholder from reappearing in the splash.
