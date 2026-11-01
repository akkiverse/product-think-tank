---
name: manager-run
description: Product Think Tank command /manager-run. Runs exactly one manager cycle (read board, drafts to issues, recover stuck work, work up to 3 cards with at most 1 build or release, summary starting "Needs you:"). This is the prompt of the scheduled "Think Tank manager" automation.
---

# /manager-run

Run **one** cycle of the **manager** skill (`.agents/skills/manager/SKILL.md`), steps 0 and a–e, then stop.

- Never more than 3 cards, never more than 1 build or release, never touch Parked.
- Never move cards into Approved: build / Approved: release / Rollback (except the manager's
  `--recovery` move from Building).
- Never merge, create repos/accounts, spend money or handle secrets.
- The final message is the summary; it starts with `Needs you:` whenever something waits for Abhishek.
