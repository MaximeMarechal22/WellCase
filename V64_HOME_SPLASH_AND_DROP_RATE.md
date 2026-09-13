# V64 — Home / Arsenal Splash / Drop Rate

- Home page rebuilt as a clean landing page with **no case cards, case images or case previews**.
- Case cards no longer display a "VOIR LES DROPS" button: clicking the card opens the drop-probability modal.
- Arsenal splash now uses dedicated artwork for all five categories: pistol, rifle, sniper, knife and gloves. Pistol and sniper splash artworks were rebuilt from their transparent case assets to avoid the previous generic/card rendering.
- Drop-rate modal now focuses on the probability of each individual item. Quality/condition probabilities are no longer displayed.
- Item rows show image, item name and exact drop probability; quality and rarity labels are not repeated in the drop-rate list.
- Backend Python compilation validated.
- Frontend production build could not be run in this environment because npm dependency installation timed out; the deployment Dockerfile still performs `npm ci` and `npm run build`.
