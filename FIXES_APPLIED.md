# WellCase — corrections applied

## Backend

- `backend/app/models/case.py`
  - Replaced the lossy `Case.items` many-to-many relation with `Case.case_items`.
  - Loads the association rows that contain probabilities.

- `backend/app/models/case_item.py`
  - Added the `CaseItem.item` relationship.

- `backend/app/schemas/case.py`
  - Added `CaseContentItem` with item data + probability.
  - `CaseWithItems.items` now exposes real case contents.
  - Standardized Pydantic v2 `from_attributes` configuration.

- `backend/app/api/cases.py`
  - Fixed missing `user` import.
  - `/cases/{case_id}` now returns real case contents and probabilities.
  - Removed reliance on the old lossy `Case.items` relationship.
  - Updated Pydantic v2 serialization.

- `backend/app/api/items.py`
  - Fixed missing `user` import.
  - Moved `/category/...` and `/rarity/...` before `/{item_id}`.
  - Updated Pydantic v2 serialization.

- `backend/app/api/openings.py`
  - Backend remains the single source of truth for the winning item.
  - Uses weighted random selection from valid case items.
  - Rejects invalid/zero probability pools.
  - Fixed `virtual_balance_before` (it previously added the case price incorrectly).
  - Returns the won item in the opening response.
  - Keeps inventory update and balance update in the same DB transaction.

## Frontend

- `frontend/src/components/CaseOpeningAnimation.js`
  - Rebuilt the roulette as a real horizontal track.
  - Generates 52 visual slots.
  - Places the backend winner at a known final index.
  - Calculates the final `translateX` so the winner lands under the center indicator.
  - Uses a smooth 5.6s easing animation.
  - Shows the final won item after the roll.
  - Handles API/opening errors visibly.

- `frontend/src/components/CaseOpeningAnimation.css`
  - Replaced the old vertical `translateY` animation.
  - Added horizontal flex track, viewport, central pointer, fade masks and winner styling.

- `frontend/src/pages/CaseDetailPage.js`
  - Removed hardcoded case contents.
  - Displays the actual backend items, probabilities, values and images.
  - Uses the backend-supported single-opening action instead of fake multi-open buttons.

- `frontend/src/pages/InventoryPage.js`
  - Removed references to backend fields that do not exist (`isStatTrak`, `weapon`).
  - Uses the real item category.
  - Passes the actual item object to the detail modal.
  - Upgrade action now navigates to `/upgrade`.

- `frontend/src/components/SkinDetailModal.js`
  - Removed unsupported fields (`weapon`, `exterior`, `collection`).
  - Displays category and virtual value from the real Item model.

- `frontend/src/pages/UpgradePage.js`
  - Changed source-item selection to a single `selectedItemId`, matching backend behavior.
  - Removed unsupported StatTrak display.
  - Fixed upgrade button disabled state.

## Validation

- Python source compilation: passed with `python3 -m compileall -q backend/app`.
- React production build: passed with the installed React Scripts executable.

## Remaining asset issue

The database references real case/item image paths, but the original archive does not contain those real images. `ImageWithFallback` therefore still supplies a fallback image until the missing assets are added under `frontend/public/images/cases/` and `frontend/public/images/items/`.
