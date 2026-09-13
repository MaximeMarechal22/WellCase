# WellCase V35

## Drop rates
- Highest rarity in a case is now intentionally very rare: ~0.15% in the cheapest cases and up to ~0.50% in 5,000€+ cases.
- More expensive cases increase the probability mass allocated to the rarest tier while keeping jackpots scarce.
- The same server-side distribution is used for single and ×3/×5 openings.
- Case detail probabilities now match the roll logic exactly.

## Arsenal splash
- Added dedicated cinematic splash assets for Rifle Arsenal Case, Knife Arsenal Case and Gloves Arsenal Case.
- Splash resolver uses the case name first, preventing stale DB image_url values from selecting the wrong visual.
- Splash artwork is bundled into React and also copied to public assets.
