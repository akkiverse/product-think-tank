---
name: board
description: Product Think Tank command /board. Shows the Product Think Tank board as a short table (title, status, next step, link), grouped in column order.
---

# /board

1. `python3 scripts/board.py list --json`
2. Show one markdown table, sorted by column order (Inbox, Thinking, Needs you, Approved: build, Building,
   Check preview, Approved: release, Live, Parked, Rollback), then Priority:

   | Title | Status | Next step | Link |
   |---|---|---|---|

   Drafts show "(draft)" as the link. Leave out nothing; if more than 30 cards, collapse Live and Parked to
   a count.
3. Under the table, one line: **Needs you:** the cards in Needs you / Check preview (or "nothing").
   Change nothing on the board.
