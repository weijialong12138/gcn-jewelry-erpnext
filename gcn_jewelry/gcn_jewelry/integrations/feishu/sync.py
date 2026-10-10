from __future__ import annotations

import frappe

from .client import FeishuClient
from .mapping import CARGO_FIELD_MAP, INVENTORY_FIELD_MAP, map_fields


def _config():
    config = frappe.conf.get("gcn_jewelry_feishu") or {}
    if not config.get("app_id") or not config.get("app_secret"):
        raise ValueError("Set gcn_jewelry_feishu.app_id/app_secret in site config")
    return config


def _source_config(name, config):
    value = (config.get("tables") or {}).get(name) or {}
    if not value.get("app_token") or not value.get("table_id"):
        raise ValueError(f"Missing Feishu table configuration: {name}")
    return value


def _upsert_sync_record(source_table, row_id, modified_at, payload):
    existing = frappe.db.exists(
        "Feishu Sync Record",
        {"source_table": source_table, "source_row_id": row_id},
    )
    doc = frappe.get_doc("Feishu Sync Record", existing) if existing else frappe.new_doc("Feishu Sync Record")
    doc.source_table = source_table
    doc.source_row_id = row_id
    doc.source_modified_at = modified_at
    doc.sync_status = "Synced"
    doc.payload_json = frappe.as_json(payload)
    doc.save(ignore_permissions=True)
    return doc.name


def _sync_table(name, field_map, config):
    table = _source_config(name, config)
    client = FeishuClient(config["app_id"], config["app_secret"])
    page_token = None
    count = 0
    while True:
        data = client.list_records(table["app_token"], table["table_id"], page_token)
        for record in data.get("items", []):
            fields = record.get("fields") or {}
            mapped = map_fields(fields, field_map)
            _upsert_sync_record(
                name,
                record.get("record_id"),
                record.get("last_modified_time"),
                {"fields": fields, "mapped": mapped},
            )
            count += 1
        page_token = data.get("page_token")
        if not data.get("has_more") or not page_token:
            break
    return count


def sync_full():
    config = _config()
    counts = {}
    for name, field_map in (
        ("cargo", CARGO_FIELD_MAP),
        ("inventory", INVENTORY_FIELD_MAP),
    ):
        try:
            counts[name] = _sync_table(name, field_map, config)
        except Exception as exc:
            frappe.get_doc({
                "doctype": "Feishu Sync Log",
                "source_table": name,
                "sync_status": "Failed",
                "error_message": str(exc),
                "retry_count": 0,
            }).insert(ignore_permissions=True)
            counts[name] = 0
    frappe.db.commit()
    return counts


def sync_incremental():
    # The upsert key makes repeated reads idempotent. Add a modified-time filter
    # once each Feishu table's timestamp field is confirmed.
    return sync_full()


def enqueue_incremental():
    frappe.enqueue(
        "gcn_jewelry.integrations.feishu.sync.sync_incremental",
        queue="long",
        job_name="gcn_jewelry-feishu-incremental",
    )
