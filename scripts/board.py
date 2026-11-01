#!/usr/bin/env python3
"""board.py - the only way agents read or change the Product Think Tank board.

Uses the `gh` CLI (already signed in). Standard library only.

Usage (run from the repo root):
  python3 scripts/board.py list [--status "Needs you"] [--json]
  python3 scripts/board.py show <card> [--json]
  python3 scripts/board.py find <title> [--json]
  python3 scripts/board.py add <title> [--body TEXT | --body-file F] [--label L ...]
                                     [--status Inbox] [--draft]
  python3 scripts/board.py move <card> <status> [--recovery]
  python3 scripts/board.py set <card> <field> <value>
  python3 scripts/board.py comment <card> --done TEXT --next TEXT [--ask TEXT]
                                     [--step NAME] [--result ok|failed|recovered|waiting]
  python3 scripts/board.py comment <card> --text TEXT | --file F
  python3 scripts/board.py to-issue <card>
  python3 scripts/board.py stale [--hours 6] [--json]
  python3 scripts/board.py paused

<card> can be: an issue number ("12" or "#12"), a project item id ("PVTI_..."),
or the exact card title (case-insensitive).

Founder-only columns ("Approved: build", "Approved: release", "Rollback") cannot
be set by this script. The single exception: `move <card> "Approved: build"
--recovery` when the card is currently in "Building" (stuck-work recovery of a
card the founder already approved).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "board" / "config.json"
MARKER_RE = re.compile(r"<!--\s*tt:step=(?P<step>[\w-]+)\s+result=(?P<result>[\w-]+)\s*-->")
RESULTS = ("ok", "failed", "recovered", "waiting")


class BoardError(Exception):
    """A problem the user/agent should read; printed without a traceback."""


# --------------------------------------------------------------------------- gh

def run_gh(args: list[str], stdin: str | None = None) -> str:
    """Run a gh command and return stdout. The only place that touches the network."""
    try:
        proc = subprocess.run(
            ["gh", *args], input=stdin, capture_output=True, text=True, check=False
        )
    except FileNotFoundError as exc:  # pragma: no cover - environment problem
        raise BoardError("The GitHub CLI 'gh' is not installed.") from exc
    if proc.returncode != 0:
        raise BoardError(f"gh {' '.join(args[:2])} failed: {proc.stderr.strip()}")
    return proc.stdout


def graphql(query: str, variables: dict | None = None) -> dict:
    body = json.dumps({"query": query, "variables": variables or {}})
    out = json.loads(run_gh(["api", "graphql", "--input", "-"], stdin=body))
    if out.get("errors"):
        raise BoardError("GitHub API error: " + "; ".join(e.get("message", "") for e in out["errors"]))
    return out["data"]


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


# ------------------------------------------------------------------- queries

PROJECT_Q = """
query($owner: String!, $title: String!) {
  user(login: $owner) {
    projectsV2(first: 20, query: $title) { nodes { id number title url } }
  }
}"""

FIELDS_Q = """
query($id: ID!) {
  node(id: $id) {
    ... on ProjectV2 {
      fields(first: 50) {
        nodes {
          ... on ProjectV2FieldCommon { id name dataType }
          ... on ProjectV2SingleSelectField { options { id name } }
        }
      }
    }
  }
}"""

ITEMS_Q = """
query($id: ID!, $after: String) {
  node(id: $id) {
    ... on ProjectV2 {
      items(first: 100, after: $after) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id createdAt updatedAt isArchived
          content {
            __typename
            ... on DraftIssue { id title body updatedAt }
            ... on Issue {
              id number title body url state updatedAt
              repository { nameWithOwner }
              labels(first: 20) { nodes { name } }
              comments(last: 20) { nodes { body createdAt } }
            }
            ... on PullRequest { id number title url state updatedAt }
          }
          fieldValues(first: 30) {
            nodes {
              __typename
              ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2FieldCommon { name } } }
              ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2FieldCommon { name } } }
              ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2FieldCommon { name } } }
            }
          }
        }
      }
    }
  }
}"""

SET_VALUE_M = """
mutation($project: ID!, $item: ID!, $field: ID!, $value: ProjectV2FieldValue!) {
  updateProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item, fieldId: $field, value: $value}) {
    projectV2Item { id }
  }
}"""

ADD_DRAFT_M = """
mutation($project: ID!, $title: String!, $body: String) {
  addProjectV2DraftIssue(input: {projectId: $project, title: $title, body: $body}) { projectItem { id } }
}"""

ADD_ITEM_M = """
mutation($project: ID!, $content: ID!) {
  addProjectV2ItemById(input: {projectId: $project, contentId: $content}) { item { id } }
}"""

REPO_Q = """
query($owner: String!, $name: String!) { repository(owner: $owner, name: $name) { id } }"""

ISSUE_Q = """
query($owner: String!, $name: String!, $number: Int!) {
  repository(owner: $owner, name: $name) { issue(number: $number) { id url } }
}"""

CONVERT_M = """
mutation($item: ID!, $repo: ID!) {
  convertProjectV2DraftIssueItemToIssue(input: {itemId: $item, repositoryId: $repo}) {
    item { id content { ... on Issue { number url } } }
  }
}"""


# ---------------------------------------------------------------------- model

def parse_item(node: dict) -> dict:
    """Flatten a GraphQL project item into a simple card dict."""
    content = node.get("content") or {}
    kind = content.get("__typename", "Unknown")
    fields: dict[str, object] = {}
    for fv in (node.get("fieldValues") or {}).get("nodes", []):
        name = ((fv or {}).get("field") or {}).get("name")
        if not name:
            continue
        for key in ("name", "text", "number"):
            if key in fv and fv[key] is not None:
                fields[name] = fv[key]
                break
    comments = ((content.get("comments") or {}).get("nodes")) or []
    updated = max(filter(None, [node.get("updatedAt"), content.get("updatedAt")]), default=None)
    return {
        "item_id": node["id"],
        "kind": kind,  # DraftIssue | Issue | PullRequest
        "title": content.get("title", ""),
        "body": content.get("body", ""),
        "number": content.get("number"),
        "url": content.get("url"),
        "content_id": content.get("id"),
        "state": content.get("state"),
        "labels": [l["name"] for l in ((content.get("labels") or {}).get("nodes") or [])],
        "comments": comments,
        "created_at": node.get("createdAt"),
        "updated_at": updated,
        "archived": node.get("isArchived", False),
        "status": fields.get("Status"),
        "fields": fields,
    }


class Board:
    def __init__(self, config: dict | None = None):
        self.cfg = config or load_config()
        self.owner = self.cfg["owner"]
        self._project: dict | None = None
        self._fields: dict | None = None

    # -- lookups
    @property
    def project(self) -> dict:
        if self._project is None:
            nodes = graphql(PROJECT_Q, {"owner": self.owner, "title": self.cfg["project_title"]})
            nodes = nodes["user"]["projectsV2"]["nodes"]
            match = [p for p in nodes if p["title"] == self.cfg["project_title"]]
            if not match:
                raise BoardError(
                    f"Project '{self.cfg['project_title']}' not found for {self.owner}. "
                    "Run scripts/board_setup.py first."
                )
            self._project = match[0]
        return self._project

    @property
    def fields(self) -> dict:
        if self._fields is None:
            data = graphql(FIELDS_Q, {"id": self.project["id"]})
            self._fields = {f["name"]: f for f in data["node"]["fields"]["nodes"] if f.get("name")}
        return self._fields

    def items(self) -> list[dict]:
        cards, after = [], None
        while True:
            data = graphql(ITEMS_Q, {"id": self.project["id"], "after": after})
            page = data["node"]["items"]
            cards += [parse_item(n) for n in page["nodes"] if not n.get("isArchived")]
            if not page["pageInfo"]["hasNextPage"]:
                return cards
            after = page["pageInfo"]["endCursor"]

    def resolve(self, ref: str, cards: list[dict] | None = None) -> dict:
        cards = cards if cards is not None else self.items()
        ref = ref.strip()
        if ref.startswith("PVTI_"):
            hits = [c for c in cards if c["item_id"] == ref]
        elif re.fullmatch(r"#?\d+", ref):
            num = int(ref.lstrip("#"))
            hits = [c for c in cards if c["kind"] == "Issue" and c["number"] == num]
        elif ref.startswith("https://github.com/"):
            hits = [c for c in cards if c["url"] == ref]
        else:
            hits = [c for c in cards if c["title"].strip().lower() == ref.lower()]
        if not hits:
            raise BoardError(f"No card matches '{ref}'.")
        if len(hits) > 1:
            raise BoardError(f"'{ref}' matches {len(hits)} cards; use the issue number instead.")
        return hits[0]

    # -- writes
    def _check_account(self) -> None:
        login = run_gh(["api", "user", "--jq", ".login"]).strip()
        if login != self.owner:
            raise BoardError(
                f"gh is signed in as '{login}', expected '{self.owner}'. "
                f"Run: gh auth switch --user {self.owner}"
            )

    def _set(self, card: dict, field_name: str, value: str) -> None:
        field = self.fields.get(field_name)
        if not field:
            raise BoardError(f"Unknown field '{field_name}'. Known: {', '.join(sorted(self.fields))}")
        dtype = field.get("dataType")
        if dtype == "SINGLE_SELECT":
            opts = {o["name"].lower(): o["id"] for o in field.get("options", [])}
            if value.lower() not in opts:
                raise BoardError(
                    f"'{value}' is not an option of {field_name}: "
                    + ", ".join(o["name"] for o in field["options"])
                )
            gql_value: dict = {"singleSelectOptionId": opts[value.lower()]}
        elif dtype == "NUMBER":
            try:
                gql_value = {"number": float(value)}
            except ValueError as exc:
                raise BoardError(f"{field_name} needs a number, got '{value}'.") from exc
        elif dtype == "TEXT":
            gql_value = {"text": value}
        else:
            raise BoardError(f"Field '{field_name}' ({dtype}) cannot be set by board.py.")
        graphql(SET_VALUE_M, {"project": self.project["id"], "item": card["item_id"],
                              "field": field["id"], "value": gql_value})

    def move(self, card: dict, status: str, recovery: bool = False) -> None:
        statuses = {s.lower(): s for s in self.cfg["statuses"]}
        if status.lower() not in statuses:
            raise BoardError(f"Unknown status '{status}'. Columns: {', '.join(self.cfg['statuses'])}")
        status = statuses[status.lower()]
        check_move_allowed(card.get("status"), status, recovery, self.cfg)
        self._check_account()
        self._set(card, "Status", status)

    def set_field(self, card: dict, field: str, value: str) -> None:
        if field.lower() == "status":
            raise BoardError("Use 'move' to change Status.")
        self._check_account()
        self._set(card, field, value)

    def comment(self, card: dict, text: str) -> None:
        if card["kind"] != "Issue":
            raise BoardError("This card is a draft. Run 'to-issue' first, then comment.")
        self._check_account()
        run_gh(["issue", "comment", str(card["number"]), "--repo", self.cfg["repo"], "--body-file", "-"],
               stdin=text)

    def add(self, title: str, body: str, labels: list[str], status: str, draft: bool) -> dict:
        if status in self.cfg["founder_only_statuses"]:
            raise BoardError(f"Agents cannot add cards straight into '{status}'.")
        self._check_account()
        if draft:
            data = graphql(ADD_DRAFT_M, {"project": self.project["id"], "title": title, "body": body})
            item_id = data["addProjectV2DraftIssue"]["projectItem"]["id"]
            card = {"item_id": item_id, "kind": "DraftIssue", "title": title, "url": None, "number": None}
        else:
            args = ["issue", "create", "--repo", self.cfg["repo"], "--title", title, "--body-file", "-"]
            for label in labels:
                args += ["--label", label]
            url = run_gh(args, stdin=body or " ").strip().splitlines()[-1]
            number = int(url.rstrip("/").split("/")[-1])
            owner, name = self.cfg["repo"].split("/")
            issue = graphql(ISSUE_Q, {"owner": owner, "name": name, "number": number})
            content_id = issue["repository"]["issue"]["id"]
            data = graphql(ADD_ITEM_M, {"project": self.project["id"], "content": content_id})
            card = {"item_id": data["addProjectV2ItemById"]["item"]["id"], "kind": "Issue",
                    "title": title, "url": url, "number": number}
        self._set(card, "Status", status)
        card["status"] = status
        return card

    def to_issue(self, card: dict) -> dict:
        if card["kind"] != "DraftIssue":
            raise BoardError(f"Card is already a {card['kind']} ({card.get('url')}).")
        self._check_account()
        owner, name = self.cfg["repo"].split("/")
        repo_id = graphql(REPO_Q, {"owner": owner, "name": name})["repository"]["id"]
        data = graphql(CONVERT_M, {"item": card["item_id"], "repo": repo_id})
        content = data["convertProjectV2DraftIssueItemToIssue"]["item"]["content"]
        return {**card, "kind": "Issue", "number": content["number"], "url": content["url"]}

    def paused(self) -> list[str]:
        out = run_gh(["issue", "list", "--repo", self.cfg["repo"], "--label", "pause-manager",
                      "--state", "open", "--json", "url", "--jq", ".[].url"])
        return [line for line in out.splitlines() if line.strip()]


# ------------------------------------------------------------- pure helpers

def check_move_allowed(current: str | None, target: str, recovery: bool, cfg: dict) -> None:
    """Enforce: only the founder moves cards into the approval/rollback columns."""
    if target not in cfg["founder_only_statuses"]:
        return
    if recovery and target == "Approved: build" and current == "Building":
        return
    raise BoardError(
        f"Only Abhishek can move cards into '{target}'. "
        "Post a comment asking him instead."
    )


def format_comment(done: str, nxt: str, ask: str | None, step: str, result: str) -> str:
    if result not in RESULTS:
        raise BoardError(f"--result must be one of {', '.join(RESULTS)}")
    lines = [f"**Done:** {done.strip()}", f"**Next:** {nxt.strip()}"]
    if ask:
        lines.append(f"**Your call:** {ask.strip()}")
    lines.append(f"<!-- tt:step={step} result={result} -->")
    return "\n\n".join(lines)


def markers(card: dict) -> list[dict]:
    found = []
    for c in card.get("comments") or []:
        for m in MARKER_RE.finditer(c.get("body", "")):
            found.append({"step": m["step"], "result": m["result"], "at": c.get("createdAt")})
    return found


def failures_since_success(card: dict) -> int:
    """Count failed/recovered markers after the most recent ok marker."""
    count = 0
    for m in markers(card):
        if m["result"] == "ok":
            count = 0
        elif m["result"] in ("failed", "recovered"):
            count += 1
    return count


def _parse_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def find_stale(cards: list[dict], hours: float, now: dt.datetime | None = None) -> list[dict]:
    """Cards in Thinking/Building with no update for `hours`, with a suggested action."""
    now = now or dt.datetime.now(dt.timezone.utc)
    back = {"Thinking": "Inbox", "Building": "Approved: build"}
    stale = []
    for card in cards:
        if card.get("status") not in back:
            continue
        updated = _parse_time(card.get("updated_at"))
        if updated is None or (now - updated) < dt.timedelta(hours=hours):
            continue
        fails = failures_since_success(card)
        action = "Needs you" if fails >= 2 else back[card["status"]]
        stale.append({**summary(card), "failures": fails, "move_to": action,
                      "idle_hours": round((now - updated).total_seconds() / 3600, 1)})
    return stale


def summary(card: dict) -> dict:
    f = card.get("fields", {})
    return {
        "card": f"#{card['number']}" if card.get("number") else card["item_id"],
        "title": card.get("title"),
        "status": card.get("status"),
        "priority": f.get("Priority"),
        "next_step": f.get("Next step"),
        "kind": card.get("kind"),
        "url": card.get("url"),
        "created_at": card.get("created_at"),
        "updated_at": card.get("updated_at"),
    }


def table(rows: list[dict]) -> str:
    if not rows:
        return "(no cards)"
    head = "| Card | Title | Status | Priority | Next step | Link |\n|---|---|---|---|---|---|"
    body = [
        f"| {r['card']} | {r['title']} | {r['status'] or '-'} | {r['priority'] or '-'} | "
        f"{r['next_step'] or '-'} | {r['url'] or '(draft)'} |"
        for r in rows
    ]
    return "\n".join([head, *body])


# ------------------------------------------------------------------------ cli

def read_text(text: str | None, path: str | None) -> str:
    if path:
        return sys.stdin.read() if path == "-" else Path(path).read_text()
    return text or ""


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="board.py", description="Product Think Tank board tool")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("list", help="list cards")
    s.add_argument("--status")
    s.add_argument("--json", action="store_true")

    s = sub.add_parser("show", help="read one card")
    s.add_argument("card")
    s.add_argument("--json", action="store_true")

    s = sub.add_parser("find", help="find cards whose title contains text")
    s.add_argument("title")
    s.add_argument("--json", action="store_true")

    s = sub.add_parser("add", help="add a card (an issue in this repo, or a draft)")
    s.add_argument("title")
    s.add_argument("--body")
    s.add_argument("--body-file")
    s.add_argument("--label", action="append", default=[])
    s.add_argument("--status", default="Inbox")
    s.add_argument("--draft", action="store_true")

    s = sub.add_parser("move", help="move a card to a column")
    s.add_argument("card")
    s.add_argument("status")
    s.add_argument("--recovery", action="store_true",
                   help="manager stuck-work recovery: Building -> Approved: build only")

    s = sub.add_parser("set", help="set a field (Stage, Priority, Score, Verdict, Product, Next step)")
    s.add_argument("card")
    s.add_argument("field")
    s.add_argument("value")

    s = sub.add_parser("comment", help="comment on the card's issue")
    s.add_argument("card")
    s.add_argument("--done")
    s.add_argument("--next")
    s.add_argument("--ask")
    s.add_argument("--step", default="agent")
    s.add_argument("--result", default="ok")
    s.add_argument("--text")
    s.add_argument("--file")

    s = sub.add_parser("to-issue", help="turn a draft card into an issue in this repo")
    s.add_argument("card")

    s = sub.add_parser("stale", help="cards stuck in Thinking/Building")
    s.add_argument("--hours", type=float, default=6)
    s.add_argument("--json", action="store_true")

    sub.add_parser("paused", help="exit 3 if the manager is paused")
    return p


def main(argv: list[str] | None = None, board: Board | None = None) -> int:
    args = build_parser().parse_args(argv)
    b = board or Board()
    try:
        if args.cmd == "list":
            cards = b.items()
            if args.status:
                cards = [c for c in cards if (c["status"] or "").lower() == args.status.lower()]
            rows = [summary(c) for c in cards]
            print(json.dumps(rows, indent=2) if args.json else table(rows))
        elif args.cmd == "show":
            card = b.resolve(args.card)
            if args.json:
                print(json.dumps({**card, "markers": markers(card)}, indent=2))
            else:
                print(f"{card['title']}  [{card['status']}]  {card.get('url') or '(draft)'}")
                for k, v in sorted(card["fields"].items()):
                    if k not in ("Title", "Status"):
                        print(f"  {k}: {v}")
                print("\n" + (card["body"] or "(no description)"))
                for c in card["comments"][-5:]:
                    print(f"\n--- comment {c['createdAt']}\n{c['body']}")
        elif args.cmd == "find":
            needle = args.title.lower()
            rows = [summary(c) for c in b.items() if needle in c["title"].lower()]
            print(json.dumps(rows, indent=2) if args.json else table(rows))
        elif args.cmd == "add":
            card = b.add(args.title, read_text(args.body, args.body_file), args.label,
                         args.status, args.draft)
            print(json.dumps(card, indent=2))
        elif args.cmd == "move":
            card = b.resolve(args.card)
            b.move(card, args.status, args.recovery)
            print(f"Moved '{card['title']}' -> {args.status}")
        elif args.cmd == "set":
            card = b.resolve(args.card)
            b.set_field(card, args.field, args.value)
            print(f"Set {args.field} = {args.value} on '{card['title']}'")
        elif args.cmd == "comment":
            card = b.resolve(args.card)
            if args.text or args.file:
                text = read_text(args.text, args.file)
            elif args.done and args.next:
                text = format_comment(args.done, args.next, args.ask, args.step, args.result)
            else:
                raise BoardError("Give --done and --next (preferred), or --text/--file.")
            b.comment(card, text)
            print(f"Commented on {card['url']}")
        elif args.cmd == "to-issue":
            card = b.to_issue(b.resolve(args.card))
            print(f"Now issue #{card['number']}: {card['url']}")
        elif args.cmd == "stale":
            rows = find_stale(b.items(), args.hours)
            if args.json:
                print(json.dumps(rows, indent=2))
            else:
                for r in rows:
                    print(f"{r['card']} {r['title']} [{r['status']}] idle {r['idle_hours']}h, "
                          f"failures {r['failures']} -> move to {r['move_to']}")
                if not rows:
                    print("(nothing stuck)")
        elif args.cmd == "paused":
            urls = b.paused()
            if urls:
                print("PAUSED by: " + ", ".join(urls))
                return 3
            print("not paused")
    except BoardError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
