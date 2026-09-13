# WellCase V23

- Battle Pass cosmetic progression: purple name, NEON theme, gold name + ELITE badge at completion.
- Prestige system: 5,000 season XP threshold, lifetime XP retained, +5% XP per prestige, prestige cosmetic identity.
- Player Market: list one inventory unit at a custom price, buy from other players, cancel listings and transfer inventory/cash atomically.
- Weapon classes: Assault Rifles, SMGs, Snipers, Pistols, Knives, Gloves.
- Collection completion page with class progress and completion bonuses.
- Completed collections grant +25 XP on future matching drops.
- More conservative case economy and much rarer high-multiple jackpots, including revised new-case pools.
- New weapon images are imported into the React bundle so Vercel/static path issues cannot blank them.
- Best-drop profile image now uses the actual history item image rather than a hard-coded filename.
- Removed browser alert/confirm popups from the main gameplay flows; feedback is inline.
- Opening overlay cannot be accidentally dismissed while the server has already charged the case.
- Global cinematic visual polish and improved marketplace/profile/progression surfaces.
- Leaderboard now exposes avatar, cosmetic name color, badge and prestige level.
- All schema additions have startup migrations for existing SQLite databases.
