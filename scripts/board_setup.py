#!/usr/bin/env python3
"""board_setup.py - create the "Product Think Tank" GitHub Project (run once, by Abhishek).

Safe to run more than once: it reuses what already exists.

  python3 scripts/board_setup.py --dry-run   # show what would happen, change nothing
  python3 scripts/board_setup.py             # do it

What it does (all with the gh CLI, as user akkiverse):
  1. Checks gh is signed in as akkiverse with the 'project' permission.
  2. Creates the project (or reuses it) and links it to akkiverse/product-think-tank.
  3. Sets the Status columns, in order: Inbox ... Rollback.
  4. Adds the fields Stage, Priority, Score, Verdict, Product, Next step.
  5. Adds repo labels: idea, product, suggested-by-inspect, pause-manager.
  6. Tries to create the "Board" and "Table" views (GitHub may not allow this by script).
  7. Prints the few clicks that only the GitHub website can do.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from board import FIELDS_Q, PROJECT_Q, BoardError, graphql, load_config, run_gh  # noqa: E402

COLORS = ["GRAY", "BLUE", "PURPLE", "YELLOW", "ORANGE", "PINK", "GREEN", "GREEN", "GRAY", "RED"]
STATUS_HELP = {
    "Inbox": "New ideas and requests",
    "Thinking": "Strategist or analyst at work",
    "Needs you": "Waiting for Abhishek's decision",
    "Approved: build": "Abhishek approved the build (founder only)",
    "Building": "Engineer is building",
    "Check preview": "Preview link ready for Abhishek",
    "Approved: release": "Abhishek approved the release (founder only)",
    "Live": "Released and live",
    "Parked": "On hold - agents never touch",
    "Rollback": "Abhishek asked for a rollback (founder only)",
}

UPDATE_FIELD_M = """
mutation($field: ID!, $options: [ProjectV2SingleSelectFieldOptionInput!]) {
  updateProjectV2Field(input: {fieldId: $field, singleSelectOptions: $options}) {
    projectV2Field { ... on ProjectV2SingleSelectField { id } }
  }
}"""

CREATE_FIELD_M = """
mutation($project: ID!, $name: String!, $type: ProjectV2CustomFieldType!,
         $options: [ProjectV2SingleSelectFieldOptionInput!]) {
  createProjectV2Field(input: {projectId: $project, name: $name, dataType: $type,
                               singleSelectOptions: $options}) {
    projectV2Field { ... on ProjectV2FieldCommon { id name } }
  }
}"""


def say(msg: str) -> None:
    print(msg, flush=True)


def check_auth(owner: str) -> None:
    login = run_gh(["api", "user", "--jq", ".login"]).strip()
    if login != owner:
        raise BoardError(f"gh is signed in as '{login}'. Run: gh auth switch --user {owner}")
    status = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
    if "'project'" not in (status.stdout + status.stderr):
        raise BoardError("gh is missing the 'project' permission. Run: gh auth refresh -s project")
    say(f"OK  signed in as {owner} with project permission")


def find_project(cfg: dict) -> dict | None:
    nodes = graphql(PROJECT_Q, {"owner": cfg["owner"], "title": cfg["project_title"]})
    for p in nodes["user"]["projectsV2"]["nodes"]:
        if p["title"] == cfg["project_title"]:
            return p
    return None


def ensure_project(cfg: dict, dry: bool) -> dict | None:
    project = find_project(cfg)
    if project:
        say(f"OK  project exists: #{project['number']} {project['url']}")
        return project
    if dry:
        say(f"DRY would create project '{cfg['project_title']}' for {cfg['owner']}")
        return None
    out = run_gh(["project", "create", "--owner", cfg["owner"], "--title", cfg["project_title"],
                  "--format", "json"])
    created = json.loads(out)
    say(f"NEW project #{created['number']} {created.get('url', '')}")
    return find_project(cfg)


def ensure_link(cfg: dict, project: dict, dry: bool) -> None:
    if dry:
        say(f"DRY would link project to {cfg['repo']}")
        return
    try:
        run_gh(["project", "link", str(project["number"]), "--owner", cfg["owner"], "--repo", cfg["repo"]])
        say(f"OK  linked to {cfg['repo']}")
    except BoardError as exc:
        if "already" in str(exc).lower():
            say(f"OK  already linked to {cfg['repo']}")
        else:
            raise


def options(names: list[str], colors: list[str] | None = None, help_: dict | None = None) -> list[dict]:
    return [{"name": n, "color": (colors[i] if colors else "GRAY"), "description": (help_ or {}).get(n, "")}
            for i, n in enumerate(names)]


def ensure_fields(cfg: dict, project: dict, dry: bool) -> None:
    fields = {f["name"]: f for f in graphql(FIELDS_Q, {"id": project["id"]})["node"]["fields"]["nodes"]
              if f.get("name")}
    status = fields.get("Status")
    current = [o["name"] for o in (status or {}).get("options", [])]
    if current == cfg["statuses"]:
        say("OK  Status columns already correct")
    elif dry:
        say(f"DRY would replace Status options {current} with {cfg['statuses']}")
    else:
        graphql(UPDATE_FIELD_M, {"field": status["id"],
                                 "options": options(cfg["statuses"], COLORS, STATUS_HELP)})
        say("NEW Status columns: " + " | ".join(cfg["statuses"]))

    for name, spec in cfg["fields"].items():
        if name in fields:
            say(f"OK  field '{name}' exists")
            continue
        if dry:
            say(f"DRY would create field '{name}' ({spec['type']}) {spec.get('options', '')}")
            continue
        variables = {"project": project["id"], "name": name, "type": spec["type"], "options": None}
        if spec["type"] == "SINGLE_SELECT":
            variables["options"] = options(spec["options"])
        graphql(CREATE_FIELD_M, variables)
        say(f"NEW field '{name}'")


def ensure_labels(cfg: dict, dry: bool) -> None:
    for name, spec in cfg["labels"].items():
        if dry:
            say(f"DRY would create/update label '{name}'")
            continue
        run_gh(["label", "create", name, "--repo", cfg["repo"], "--color", spec["color"],
                "--description", spec["description"], "--force"])
        say(f"OK  label '{name}'")


def try_views(cfg: dict, project: dict, dry: bool) -> list[str]:
    """Try the REST views endpoint. Returns names of views that still need manual setup."""
    todo = []
    for name, layout in (("Board", "board"), ("Table", "table")):
        if dry:
            say(f"DRY would try to create view '{name}' ({layout})")
            todo.append(name)
            continue
        body = json.dumps({"name": name, "layout": layout})
        try:
            run_gh(["api", "--method", "POST",
                    f"/users/{cfg['owner']}/projectsV2/{project['number']}/views",
                    "-H", "X-GitHub-Api-Version: 2022-11-28", "--input", "-"], stdin=body)
            say(f"NEW view '{name}'")
        except BoardError:
            say(f"--  view '{name}' must be created on the website (GitHub API refused)")
            todo.append(name)
    return todo


def manual_steps(project: dict | None, views_todo: list[str]) -> str:
    url = (project or {}).get("url", "https://github.com/users/akkiverse/projects")
    steps = [f"Open {url}"]
    if "Board" in views_todo:
        steps.append('Views: click "+ New view" > Board. Name it "Board". Column field: Status.')
    if "Table" in views_todo:
        steps.append('Click "+ New view" > Table. Name it "Table". Click "+" at the right of the '
                     "header and tick every field (Status, Stage, Priority, Score, Verdict, Product, Next step).")
    steps += [
        'Delete the default "View 1" if it is still there (its "..." menu > Delete view).',
        'Top-right "..." > Workflows > "Item added to project": set Status = Inbox, then "Save and turn on".',
        'In the same Workflows page, turn OFF "Item closed" and "Pull request merged" '
        '(they point at a "Done" column that no longer exists).',
    ]
    return "\n".join(f"  {i}. {s}" for i, s in enumerate(steps, 1))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="show what would happen, change nothing")
    args = ap.parse_args()
    cfg = load_config()
    try:
        check_auth(cfg["owner"])
        project = ensure_project(cfg, args.dry_run)
        if project:
            ensure_link(cfg, project, args.dry_run)
            ensure_fields(cfg, project, args.dry_run)
        ensure_labels(cfg, args.dry_run)
        views_todo = try_views(cfg, project, args.dry_run) if project else ["Board", "Table"]
    except BoardError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    say("\nLast steps on the GitHub website (GitHub does not allow these by script):")
    say(manual_steps(project, views_todo))
    say("\nThen check: python3 scripts/board.py list")
    return 0


if __name__ == "__main__":
    sys.exit(main())
