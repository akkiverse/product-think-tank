---
name: start-session
description: Product Think Tank command /start-session. Pulls this repo and every repo in products/, reads TASKS.md and the newest docs/phases/PHASE-N.md, lists cards in Needs you and Check preview, then tells Abhishek in 3-5 lines what changed, what needs him and what comes next.
---

# /start-session

1. **Pull.**
   ```bash
   git pull --ff-only
   for d in products/*/; do [ -d "$d/.git" ] && git -C "$d" pull --ff-only || true; done
   gh api user --jq .login   # must be akkiverse; if not: tell Abhishek "gh auth switch --user akkiverse"
   ```
   If a pull fails (local changes, diverged), don't force anything; mention it in the summary.
2. **Read** `TASKS.md` and the newest phase note: `ls docs/phases/PHASE-*.md | sort -V | tail -1`
   (none yet is fine).
3. **Board:**
   ```bash
   python3 scripts/board.py list --status "Needs you"
   python3 scripts/board.py list --status "Check preview"
   ```
   Also note what changed since the last phase note (`git log --since=<its date> --oneline`, merged PRs).
4. **Tell Abhishek in 3–5 lines** (plain words):
   - **Changed:** …
   - **Needs you:** card links + the decision in a few words (or "nothing").
   - **Next:** what you'll do, and one recommendation. Then wait for his go.
