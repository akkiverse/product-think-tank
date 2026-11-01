---
name: rollback
description: Product Think Tank command /rollback <card>. Checks the card is in "Rollback", then runs the engineer in Rollback mode (Vercel Instant Rollback, then a revert PR on main). Refuses otherwise.
---

# /rollback <card>

1. `python3 scripts/board.py show <card> --json`.
2. **Gate:** Status must be exactly **Rollback**. If not, reply: "<card> is in <status>. Move it to Rollback
   on the board and I'll roll it back." Stop; change nothing.
3. Run the **engineer** skill, **Mode 3: Rollback**.
4. Reply in 3 lines: what is live now · revert PR for him to merge · the follow-up (promote after merge).
