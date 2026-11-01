---
name: build
description: Product Think Tank command /build <card>. Checks the card is in "Approved: build", then runs the engineer in Build & test mode (spec-driven PR plus Vercel preview link). Refuses otherwise.
---

# /build <card>

1. `python3 scripts/board.py show <card> --json`.
2. **Gate:** Status must be exactly **Approved: build**. If not, reply: "<card> is in <status>. I only build
   cards you've moved to Approved: build." Stop; change nothing.
3. Run the **engineer** skill, **Mode 1: Build & test** (it does the pre-work check first).
4. Reply in 3 lines: PR link · preview link · what to check.
