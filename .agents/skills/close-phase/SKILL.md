---
name: close-phase
description: Product Think Tank command /close-phase. Writes docs/phases/PHASE-N.md (where things stand, what was built, decisions, gotchas, how to start the next phase; under 2 pages), updates TASKS.md, pushes via a PR, and gives Abhishek the starter message for the next conversation.
---

# /close-phase

1. `git switch main && git pull --ff-only`. N = highest existing `docs/phases/PHASE-N.md` + 1 (first is 1).
2. Gather: TASKS.md, `python3 scripts/board.py list --json`, merged PRs since the last phase
   (`gh pr list --state merged --search "merged:>=<date>"`), catalog changes, ADRs added.
3. Branch `chore/close-phase-N`. Write `docs/phases/PHASE-N.md` (**under 2 pages**, plain words):
   - **Where things stand**: board snapshot (count per column + cards in Needs you / Check preview).
   - **What was built**: products, releases, PR links.
   - **Decisions**: with links to ADRs / card comments.
   - **Gotchas**: what tripped us up, and the fix.
   - **How to start the next phase**: first 3 steps.
4. Update `TASKS.md`: tick finished items (`- [x] … (YYYY-MM-DD, <PR link>)`), move them to Done, add new ones.
5. Commit, push, open the PR "Close phase N". Never merge.
6. Give Abhishek the **starter message** for the next conversation, in a code block, e.g.:
   ```text
   /start-session
   We're starting phase <N+1> of Product Think Tank. Read docs/phases/PHASE-<N>.md first.
   Focus: <top 1-2 goals>.
   ```
