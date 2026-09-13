# WellCase — Premium case opening + upgrade fixes

- Case opening is server-authoritative: the reward is selected before the roulette starts.
- Roulette completion uses a single timer lifecycle; the status changes from ROLLING to YOU WON only after the animation finishes.
- The winner slot is visually emphasized only after the wheel stops.
- Case probabilities exposed by the API are normalized to 100% even when database weights do not sum to 100.
- Upgrade requires an owned source item and a strictly more valuable target.
- Upgrade chance is calculated from source/target value, capped at 95% and floored at 1%.
- Failed upgrades consume the source item; successful upgrades add the target item.
- Upgrade UI only shows valid higher-value targets and displays the calculated chance.
- Added all 22 item images and all 5 case images from the project visual pack.
- Removed the repeated virtual-currency disclaimer banners.
- Updated Pydantic v2 schemas to use from_attributes.
