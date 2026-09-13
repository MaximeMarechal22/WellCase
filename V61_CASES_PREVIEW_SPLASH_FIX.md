V61 fixes:
- Case preview is rendered through React portal directly into document.body.
- Removed non-useful preview hint text.
- Preview shows per-item probabilities immediately from catalogue data.
- Arsenal visual artwork uses five dedicated generated local PNG assets, not legacy type_* or old splash composites.
- Cases catalog always synchronizes before GET /cases/.
- Legacy duplicate knife cases are deactivated.
