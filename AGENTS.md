# AGENTS.md: house rules for coding agents

These rules apply to any coding agent working in **Product Think Tank by AkkiVerse** and in every
product repo it builds (`products/<name>`). Board, approval and founder rules live in
`.agents/rules/think-tank.md`; this file is about *how work is done*.

## 1. Spec-driven work (product repos)

Every change, however small, carries this paper trail inside the product repo:

| Artifact | Where | Notes |
|---|---|---|
| Change request | `docs/changes/CR-NNNN-<short-name>.md` | Use `templates/CR.md`. States the why, scope, out of scope, and the acceptance criteria it adds or changes. |
| Spec IDs | `AC-x.y` | `x` = user story number from the spec, `y` = criterion. Never reuse or renumber an ID; retire it with "(removed in CR-NNNN)". |
| Changelog | `CHANGELOG.md` | One entry per CR under `## [Unreleased]` ([Keep a Changelog](https://keepachangelog.com) style). |
| Test report | `docs/test-reports/CR-NNNN.md` | Use `templates/TEST-REPORT.md`: command run, pass/fail per AC, anything skipped and why. |
| ADR | `docs/adr/ADR-NNNN-<title>.md` | Only for big decisions (new framework, database, data model, paid service, auth). Use `templates/ADR.md`. |

A new product starts with `docs/SPEC.md` (copied from the idea's `SPEC.md`), `CR-0001-initial-build.md`,
`README.md`, `CHANGELOG.md`, `.env.example` and `vercel.json` if needed.

## 2. One task = one branch = one pull request

- Branch name: `cr/NNNN-short-name` (lowercase, hyphens).
- **Next free CR number:** the highest `CR-NNNN` found on `main` **and** in every open pull request
  (title, branch name and changed files), plus one. Check with:
  ```bash
  git fetch origin && git ls-tree -r --name-only origin/main docs/changes | grep -o 'CR-[0-9]\{4\}'
  gh pr list --state open --json number,title,headRefName,files
  ```
- PR title: `CR-NNNN: <short summary>`. The PR body links the CR, lists ACs covered, the test report and
  the preview link.
- Never push to `main`. Never merge a pull request; Abhishek merges.
- Before starting: `git fetch`, list open PRs and branches. If anyone else is on the same thing, stop and ask.

In the think-tank repo itself the branches are `idea/<slug>`, `inspect/<name>`, `catalog/<name>-v<version>`,
`chore/<short-name>`; the same one-task-one-PR rule applies.

## 3. Tests

- Test names include their AC: `test_ac_2_1_user_can_export_csv` (Python) or
  `it("AC-2.1 user can export CSV")` (JS). Every AC in the CR has at least one test.
- **All tests must pass** before a PR is opened or marked ready. No skipped tests without a reason in the
  test report.
- **Outside services are mocked** in tests: Vercel, payment, email, AI model APIs, third-party HTTP. Tests
  never need real keys or network.
- Python: `pytest`. JS: the repo's existing runner (`vitest` preferred for new repos).

## 4. Stack defaults

- Back end in **Python**: FastAPI (APIs) or Streamlit (data apps, simple tools).
- **React or Vue only** when a rich UI is truly needed; otherwise server-rendered or Streamlit.
- Deploy on **Vercel, team `akkiverse`**. Each PR gets a preview deployment; `main` is production.
- Pin dependencies (`pyproject.toml` + lock file, or `package-lock.json`).

## 5. Live apps never break

- Every change is backwards compatible with what is live. Feature flags or new routes over rewrites.
- **Saved data stays readable:** schema changes only add (new tables, nullable columns) or ship with a
  tested migration *and* rollback. Never drop or rename stored data in the same release that stops using it.
- A release can always be undone with Vercel Instant Rollback plus a revert PR.

## 6. Secrets

- Never commit, print, log or paste secrets (keys, tokens, passwords, connection strings).
- `.env*` is git-ignored; commit `.env.example` with empty values and a comment per variable.
- Vercel environment variables are set by Abhishek. Tell him the variable *name* and what it is for.
- If you find a secret in code, report its file and line, never its value, and propose rotating it.

## 7. Public pages

No personal data (phone, email, home address) on any public page, README, or commit message.
