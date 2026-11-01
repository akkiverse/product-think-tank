---
name: release
description: Product Think Tank command /release <card>. Checks the card is in "Approved: release", then runs the engineer in Release mode (release notes, version bump, catalog update). Abhishek merges. Refuses otherwise.
---

# /release <card>

1. `python3 scripts/board.py show <card> --json`.
2. **Gate:** Status must be exactly **Approved: release**. If not, reply: "<card> is in <status>. I only
   release cards you've moved to Approved: release." Stop; change nothing.
3. Run the **engineer** skill, **Mode 2: Release**. Never merge; if Abhishek has already merged, do step 5
   (verify live, tag, move to Live).
4. Reply in 3 lines: version · PRs for him to merge (product first, then catalog) · what happens after.
