# WellCase V66 — splash + upgrade truth fix

- Arsenal opening splash redesigned around real weapon artwork per category (pistol/rifle/sniper/knife/gloves), instead of the old placeholder case/card artwork.
- Arsenal splash is selected from the exact clicked case object in CasesPage.
- Upgrade result visual is now server-authoritative: backend computes the success/failure and a transient landing angle in the same request; frontend animates to that exact angle.
- No database migration is required for landing_angle; it is presentation-only and is not persisted.
- The stale frontend/build directory was removed from this package so the Dockerfile must rebuild the React app from source during deployment.
