# ADR-0001: Board on GitHub Projects, employees and commands as skills

- **Status:** Accepted
- **Date:** 2026-11-01

## Context
The think tank needs a shared board Abhishek can use from the web and his phone, an audit trail for every
decision, and commands he can type (`/build`, `/manager-run` …). Antigravity marks `.agents/workflows/` as
deprecated; skills give `/name` slash commands and can be discovered by the agent.

## Options
1. **GitHub Project (v2) + issues**: free, mobile app, issue comments as audit trail, `gh` CLI already signed in.
2. A markdown board in the repo: simple, but no drag-and-drop and messy merge conflicts.
3. External tool (Linear, Trello): another account and integration.

Commands: (a) legacy workflow files, (b) skills, (c) both.

## Decision
GitHub Project v2 "Product Think Tank" owned by `akkiverse`, every card backed by an issue in this repo.
All access goes through `scripts/board.py` (standard library + `gh`), which also enforces the
founder-only columns in code. Employees **and** commands are skills in `.agents/skills/`; no workflow files.

## Consequences
- Easy approvals by drag-and-drop; history lives in issue comments.
- Built-in project workflows and (possibly) views can't be set by script; `board_setup.py` prints the clicks.
- Stuck-work detection relies on the hidden `tt:` markers in comments and item update times.
