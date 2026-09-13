# WellCase V38

- Upgrade history now persists per inventory instance via `upgrade_level`.
- Each prior successful upgrade reduces the next success chance by 15% relative.
- Successful upgrades create a new tracked inventory instance instead of merging it.
- Upgrade UI uses the tracked level and a darker jade/emerald visual palette.
- Leaderboard now displays cosmetic badges for every player, including podium.
- Arsenal case splash assets are now real, deterministic assets and the splash resolver no longer trusts stale DB image paths.

- Upgrade requests can now target an exact inventory instance, preserving its improvement history.
- Arsenal splash rendering is no longer driven by stale `image_url` fields.
