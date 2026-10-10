from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

STAGES = (
    "采购/买胚",
    "做胚/定做",
    "溜光",
    "抛光",
    "烧焊",
    "电抛",
    "电镀",
    "镶钻/粘钻",
    "清洗/手工",
    "质检",
    "入库",
    "发货",
)


def build_timeline(events: Iterable[dict]) -> list[dict]:
    ordered = sorted(
        (dict(event) for event in events),
        key=lambda event: event.get("started_at") or "",
    )
    for event in ordered:
        stage = event.get("stage")
        event["stage_order"] = STAGES.index(stage) if stage in STAGES else None
    return ordered


def stage_status(started_at, expected_at, completed_at=None, now=None) -> str:
    if completed_at:
        return "Completed"
    if not started_at:
        return "Pending"
    now = now or datetime.now(timezone.utc)
    if expected_at and expected_at < now:
        return "Overdue"
    return "In Progress"


def scan_stage_timeouts():
    try:
        import frappe
    except ImportError:
        return 0

    events = frappe.get_all(
        "Production Stage Event",
        filters={"status": ["in", ["Open", "In Progress"]]},
        fields=["name", "expected_at", "completed_at"],
    )
    now = datetime.now(timezone.utc)
    changed = 0
    for event in events:
        if event.get("expected_at") and event["expected_at"] < now and not event.get("completed_at"):
            frappe.db.set_value(
                "Production Stage Event",
                event["name"],
                {"status": "Overdue"},
                update_modified=False,
            )
            changed += 1
    if changed:
        frappe.db.commit()
    return changed


def on_work_order_update(doc, method=None):
    return None
