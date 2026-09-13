# WellCase V25

- Removed the empty PM/SMG collection from the public Collections page.
- Corrected weapon-class fallback so unknown items are not falsely classified as SMGs.
- Rebuilt item image resolution using both item ID and normalized item name before any DB image path.
- Replaced the incorrect Dragon Lore image with a real AWP-silhouette asset derived from the existing AWP artwork.
- Replaced the eight new flat schematic assets with weapon-class-correct PNG renders in the React bundle and public assets.
- Fixed daily reward date checks to use an explicit UTC day window, preventing the claim button from returning after a successful claim.
- Updated the daily reward card to disappear/turn into a claimed-state strip immediately after a successful claim.
