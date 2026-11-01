---
name: new-idea
description: Product Think Tank command /new-idea <text>. Adds a card to Inbox with Abhishek's text (as an issue in this repo), then runs the strategist on it.
---

# /new-idea <text>

1. If `<text>` is empty, ask Abhishek for the idea in one or two sentences. Stop.
2. Title: `Idea: <short summary, max 60 chars>`. Check for a duplicate:
   `python3 scripts/board.py find "<key words>"`. If a similar card exists, show it and ask whether to add
   to it instead. Stop until he answers.
3. Add the card, keeping his words exactly:
   ```bash
   python3 scripts/board.py add "Idea: <summary>" --label idea --status Inbox --body "<his text, verbatim>"
   python3 scripts/board.py set <#n> Stage Idea
   python3 scripts/board.py set <#n> Priority P2      # unless he gave a priority
   ```
4. Run the **strategist** skill on the new card (it moves the card to Thinking and comments).
5. Reply in 3 lines: card link · the one-line opportunity · next step (the analyst, on the next `/manager-run`
   or now if he says so).
