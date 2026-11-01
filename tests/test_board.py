"""Unit tests for scripts/board.py. GitHub (the gh CLI) is always mocked."""
import datetime as dt
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import board  # noqa: E402

CFG = board.load_config()


def card(**kw):
    base = {"item_id": "PVTI_1", "kind": "Issue", "title": "Idea: pet diary", "body": "my text",
            "number": 7, "url": "https://github.com/akkiverse/product-think-tank/issues/7",
            "content_id": "I_1", "state": "OPEN", "labels": [], "comments": [],
            "created_at": "2026-11-01T00:00:00Z", "updated_at": "2026-11-01T00:00:00Z",
            "archived": False, "status": "Inbox", "fields": {"Status": "Inbox"}}
    base.update(kw)
    return base


class FakeBoard(board.Board):
    """A Board whose GitHub calls are recorded instead of sent."""

    def __init__(self, cards):
        super().__init__(CFG)
        self._cards = cards
        self.calls = []
        self._project = {"id": "PVT_1", "number": 1, "title": CFG["project_title"], "url": "u"}
        self._fields = {
            "Status": {"id": "F_S", "name": "Status", "dataType": "SINGLE_SELECT",
                       "options": [{"id": f"O{i}", "name": s} for i, s in enumerate(CFG["statuses"])]},
            "Score": {"id": "F_SC", "name": "Score", "dataType": "NUMBER"},
            "Next step": {"id": "F_N", "name": "Next step", "dataType": "TEXT"},
        }

    def items(self):
        return self._cards

    def _check_account(self):
        self.calls.append(("account",))

    def _set(self, c, field, value):
        self.calls.append(("set", c["item_id"], field, value))

    def comment(self, c, text):
        if c["kind"] != "Issue":
            raise board.BoardError("draft")
        self.calls.append(("comment", c["number"], text))


# --- founder-only columns -------------------------------------------------

@pytest.mark.parametrize("target", ["Approved: build", "Approved: release", "Rollback"])
def test_rule_agents_cannot_move_into_founder_only_columns(target):
    fb = FakeBoard([card(status="Needs you")])
    assert board.main(["move", "7", target], board=fb) == 2
    assert not [c for c in fb.calls if c[0] == "set"]


def test_rule_recovery_allows_building_back_to_approved_build_only():
    board.check_move_allowed("Building", "Approved: build", True, CFG)  # no error
    with pytest.raises(board.BoardError):
        board.check_move_allowed("Check preview", "Approved: build", True, CFG)
    with pytest.raises(board.BoardError):
        board.check_move_allowed("Building", "Approved: release", True, CFG)


def test_move_to_normal_column_sets_status():
    fb = FakeBoard([card()])
    assert board.main(["move", "#7", "thinking"], board=fb) == 0
    assert ("set", "PVTI_1", "Status", "Thinking") in fb.calls


def test_move_rejects_unknown_column():
    fb = FakeBoard([card()])
    assert board.main(["move", "7", "Done"], board=fb) == 2


def test_add_refuses_founder_only_column():
    fb = FakeBoard([])
    assert board.main(["add", "x", "--status", "Rollback"], board=fb) == 2


# --- card lookup ------------------------------------------------------------

def test_resolve_by_number_title_and_item_id():
    fb = FakeBoard([card(), card(item_id="PVTI_2", number=None, kind="DraftIssue", title="Draft one")])
    assert fb.resolve("7")["item_id"] == "PVTI_1"
    assert fb.resolve("draft ONE")["item_id"] == "PVTI_2"
    assert fb.resolve("PVTI_2")["title"] == "Draft one"
    with pytest.raises(board.BoardError):
        fb.resolve("nothing")


def test_resolve_refuses_ambiguous_title():
    fb = FakeBoard([card(), card(item_id="PVTI_2", number=8)])
    with pytest.raises(board.BoardError):
        fb.resolve("Idea: pet diary")


# --- comments ---------------------------------------------------------------

def test_comment_has_done_next_ask_and_marker():
    text = board.format_comment("Wrote IDEA.md", "Analyst", "Build it? A) yes B) no. I recommend A",
                                "strategist", "ok")
    assert text.startswith("**Done:** Wrote IDEA.md")
    assert "**Next:** Analyst" in text and "**Your call:**" in text
    assert board.markers({"comments": [{"body": text, "createdAt": "t"}]}) == [
        {"step": "strategist", "result": "ok", "at": "t"}]


def test_comment_on_draft_is_refused():
    fb = FakeBoard([card(kind="DraftIssue", number=None, url=None)])
    assert board.main(["comment", "PVTI_1", "--done", "a", "--next", "b"], board=fb) == 2


def test_comment_rejects_unknown_result():
    with pytest.raises(board.BoardError):
        board.format_comment("a", "b", None, "x", "great")


# --- stuck work ---------------------------------------------------------------

def _marker(result):
    return {"body": f"x <!-- tt:step=engineer result={result} -->", "createdAt": "t"}


def test_stale_moves_back_one_step_then_to_needs_you_after_two_failures():
    now = dt.datetime(2026, 11, 1, 12, tzinfo=dt.timezone.utc)
    old = "2026-11-01T05:00:00Z"   # 7 hours idle
    fresh = "2026-11-01T10:00:00Z"  # 2 hours idle
    cards = [
        card(item_id="A", number=1, status="Thinking", updated_at=old),
        card(item_id="B", number=2, status="Building", updated_at=old, comments=[_marker("recovered")]),
        card(item_id="C", number=3, status="Building", updated_at=old,
             comments=[_marker("recovered"), _marker("failed")]),
        card(item_id="D", number=4, status="Thinking", updated_at=fresh),
        card(item_id="E", number=5, status="Inbox", updated_at=old),
    ]
    got = {r["card"]: r["move_to"] for r in board.find_stale(cards, 6, now)}
    assert got == {"#1": "Inbox", "#2": "Approved: build", "#3": "Needs you"}


def test_success_resets_failure_count():
    c = card(comments=[_marker("failed"), _marker("failed"), _marker("ok"), _marker("recovered")])
    assert board.failures_since_success(c) == 1


# --- parsing ------------------------------------------------------------------

def test_parse_item_flattens_fields():
    node = {
        "id": "PVTI_9", "createdAt": "2026-10-01T00:00:00Z", "updatedAt": "2026-10-02T00:00:00Z",
        "isArchived": False,
        "content": {"__typename": "Issue", "id": "I_9", "number": 9, "title": "T", "body": "B",
                    "url": "u", "state": "OPEN", "updatedAt": "2026-10-03T00:00:00Z",
                    "labels": {"nodes": [{"name": "idea"}]}, "comments": {"nodes": []}},
        "fieldValues": {"nodes": [
            {"__typename": "ProjectV2ItemFieldSingleSelectValue", "name": "Live", "field": {"name": "Status"}},
            {"__typename": "ProjectV2ItemFieldNumberValue", "number": 82.0, "field": {"name": "Score"}},
            {"__typename": "ProjectV2ItemFieldTextValue", "text": "Ship", "field": {"name": "Next step"}},
            {},
        ]},
    }
    c = board.parse_item(node)
    assert c["status"] == "Live" and c["fields"]["Score"] == 82.0 and c["fields"]["Next step"] == "Ship"
    assert c["updated_at"] == "2026-10-03T00:00:00Z" and c["labels"] == ["idea"]


def test_graphql_sends_variables_as_json(monkeypatch):
    seen = {}

    def fake_run(args, stdin=None):
        seen["args"], seen["stdin"] = args, stdin
        return json.dumps({"data": {"ok": True}})

    monkeypatch.setattr(board, "run_gh", fake_run)
    assert board.graphql("query { ok }", {"n": 1}) == {"ok": True}
    assert seen["args"] == ["api", "graphql", "--input", "-"]
    assert json.loads(seen["stdin"])["variables"] == {"n": 1}


def test_graphql_errors_are_reported(monkeypatch):
    monkeypatch.setattr(board, "run_gh", lambda a, stdin=None: json.dumps({"errors": [{"message": "nope"}]}))
    with pytest.raises(board.BoardError, match="nope"):
        board.graphql("query { x }")


def test_set_score_needs_a_number():
    fb = FakeBoard([card()])
    fb._set = board.Board._set.__get__(fb)  # use the real validation
    with pytest.raises(board.BoardError):
        fb._set(card(), "Score", "high")
