# V50 fixes

- `/cases/` now returns the complete case catalog with weighted drop probabilities, so previews can open immediately.
- Clicking a case preview no longer waits for a second request; the detail request is only a background refresh.
- Arsenal case visuals use the CSS/React CaseVisual renderer and have explicit sizing so Rifle/Knife/Gloves/Sniper/Pistol cases cannot collapse to an empty image area.
- Upgrade success preserves the source condition on the resulting target skin and keeps the highest upgrade history when rows merge.
- Roulette cards show the server probability under each item name when available.
