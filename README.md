# Product Think Tank by AkkiVerse

An automated product studio. AI employees take an idea from brainstorm to a live product:
**strategist → analyst → engineer**, coordinated by a **manager** that runs twice a day.
**Abhishek approves every build and every release**, and merges every pull request himself.

```text
Inbox → Thinking → Needs you → [you] Approved: build → Building → Check preview
      → [you] Approved: release → [you merge] Live        (+ Parked, [you] Rollback)
```

## Folder layout

| Path | What |
|---|---|
| `AGENTS.md` | House rules for coding agents (spec-driven work, branches, tests, secrets) |
| `.agents/rules/think-tank.md` | Always-on rules: founder preferences, hard rules, board, session start |
| `.agents/skills/` | Employees (`strategist`, `analyst`, `engineer`, `inspector`, `manager`) and commands |
| `scripts/board_setup.py` | Creates the GitHub Project board (Abhishek runs it once) |
| `scripts/board.py` | The only way agents read or change the board |
| `board/` | Board guide (`README.md`) and settings (`config.json`) |
| `ideas/<slug>/` | `IDEA.md`, `BRIEF.md`, `SPEC.md` per idea |
| `catalog/<name>/` | `PROFILE.md` per product, plus `catalog/<name>.json` |
| `templates/` | Templates for ideas, briefs, specs, CRs, ADRs, test reports, release notes, profiles |
| `docs/adr/`, `docs/phases/` | Decisions about the think tank; end-of-phase notes |
| `products/` | Local clones of product repos (git-ignored) |
| `TASKS.md` | The think tank's own task list |

## Commands

Type them in the Antigravity chat (or say "run <name>").

| Command | What it does |
|---|---|
| `/start-session` | Pull everything, read tasks and the last phase note, show what needs you |
| `/new-idea <text>` | New card in Inbox, then the strategist brainstorms it |
| `/inspect <name or link>` | Profile an existing product (read-only) into `catalog/`, suggest ideas |
| `/board` | The board as a short table |
| `/manager-run` | One manager cycle (what the schedule runs) |
| `/build <card>` | Build: only if the card is in Approved: build |
| `/release <card>` | Prepare the release: only if in Approved: release |
| `/rollback <card>` | Roll back: only if in Rollback |
| `/close-phase` | Write the phase note, update tasks, give the next conversation's starter |

`<card>` = issue number (`12`), or the card's exact title.

## How you approve

Drag cards on the board ([github.com/users/akkiverse/projects](https://github.com/users/akkiverse/projects), or the
GitHub mobile app):

- **Build:** Needs you → read the brief → merge the idea PR → drag to **Approved: build**.
- **Release:** Check preview → try the preview link → drag to **Approved: release** → merge the PR when
  the engineer says it's ready.
- **Roll back:** drag a Live card to **Rollback**.
- **No:** drag to **Parked**.

Agents can't put cards into these columns; only you can. Details: [board/README.md](board/README.md).

## Manager automation

Set up once in the app's **Automations** page:

| Setting | Value |
|---|---|
| Name | Think Tank manager |
| Schedule | 09:14 and 21:14 every day, time zone Asia/Calcutta (cron `14 9,21 * * *`) |
| Model | Gemini 3.8 Flash |
| Project | product-think-tank |
| Prompt | `/manager-run` |

Each run works at most 3 cards and at most 1 build or release, and ends with a summary that starts
**"Needs you:"** when something waits for you.

## How to pause the manager

- **Switch off** the "Think Tank manager" automation in the Automations page (switch it on again to resume).
- **From anywhere:** open an issue in this repo with the label `pause-manager`. Runs do nothing until you
  close it.

## First-time setup

See `TASKS.md` → Founder. In short: make the repo private, merge the setup PR, run
`python3 scripts/board_setup.py`, do the clicks it prints, create the automation.

Tests for the board tool: `uv run --with pytest pytest tests/`.
