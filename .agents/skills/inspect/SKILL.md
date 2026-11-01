---
name: inspect
description: Product Think Tank command /inspect <name or GitHub link>. Profiles an existing product read-only (catalog/<name>/PROFILE.md and .json), adds or refreshes its board card and suggested-idea cards, and opens a PR from inspect/<name>.
---

# /inspect <name or GitHub link>

1. If no argument: list folders in `products/` and the entries in `catalog/`, and ask which one. Stop.
2. Follow the **inspector** skill exactly (`.agents/skills/inspector/SKILL.md`).
3. Remember: read-only on the product repo; suggested ideas go to Inbox and are never built without
   Abhishek's approval; re-running refreshes, never duplicates.
4. Finish with the 5-line summary and the PR link.
