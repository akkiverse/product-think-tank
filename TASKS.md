# TASKS: Product Think Tank

Tick tasks as `- [x] … (YYYY-MM-DD, <PR link>)` and move them to **Done**.

## Founder (Abhishek)

- [ ] Make the repo private: GitHub → Settings → General → Danger Zone → Change visibility → Private
      (or `gh repo edit akkiverse/product-think-tank --visibility private --accept-visibility-change-consequences`).
- [ ] Review and merge the setup PR: https://github.com/akkiverse/product-think-tank/pull/1
- [ ] Create the board: `python3 scripts/board_setup.py --dry-run`, then `python3 scripts/board_setup.py`.
- [ ] Do the website-only board steps the script prints (views, "Item added → Inbox" workflow, turn off the
      "Done" workflows).
- [ ] Confirm the Vercel plugin (Customizations > Marketplace) is connected to team **akkiverse**.
- [ ] Create the **Think Tank manager** automation (see README "Manager automation").
- [ ] Add a first idea: `/new-idea <text>`, or `/inspect <link>` for an existing product.

## Agents

- [ ] After the board exists: run `python3 scripts/board.py list` to confirm access, and do one supervised
      `/manager-run` with Abhishek watching.

## Done

- [x] Think tank setup: rules, employees, commands, board scripts, templates (2026-11-01, https://github.com/akkiverse/product-think-tank/pull/1)
