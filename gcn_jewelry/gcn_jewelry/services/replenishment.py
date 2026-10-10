from __future__ import annotations

from statistics import median


def calculate_replenishment(
    *,
    average_daily_sales: float,
    current_stock: float,
    confirmed_inbound: float,
    reserved_stock: float = 0,
    abnormal_stock: float = 0,
    lead_time_days: float = 0,
    safety_stock_days: float = 7,
    review_period_days: float = 7,
) -> dict:
    available_stock = current_stock + confirmed_inbound - reserved_stock - abnormal_stock
    safety_stock = average_daily_sales * safety_stock_days
    reorder_point = average_daily_sales * lead_time_days + safety_stock
    suggested_qty = max(
        0,
        average_daily_sales * (lead_time_days + review_period_days)
        + safety_stock
        - available_stock
        - confirmed_inbound,
    )
    return {
        "available_stock": round(available_stock, 4),
        "safety_stock": round(safety_stock, 4),
        "reorder_point": round(reorder_point, 4),
        "suggested_qty": round(suggested_qty, 4),
        "is_below_reorder_point": available_stock < reorder_point,
    }


def median_lead_time(completed_purchase_orders: list[dict]) -> float:
    values = [
        float(row["lead_time_days"])
        for row in completed_purchase_orders[-5:]
        if row.get("lead_time_days") is not None
    ]
    return float(median(values)) if values else 0.0


def detect_anomalies(*, stock: float, sales: float, ordered: float, delivered: float, received: float, inbound_eta=None) -> list[str]:
    anomalies = []
    if stock < 0:
        anomalies.append("negative_stock")
    if stock == 0 and sales > 0:
        anomalies.append("zero_stock_with_sales")
    if delivered < ordered:
        anomalies.append("short_delivery")
    if delivered > received:
        anomalies.append("arrived_not_received")
    if inbound_eta is None and ordered > received:
        anomalies.append("inbound_without_eta")
    return anomalies


def scan_replenishment_anomalies():
    # The deterministic calculation is available first. Site-specific queries
    # can create Replenishment Anomaly documents after field mappings are confirmed.
    return None


def on_purchase_order_update(doc, method=None):
    return None


def on_purchase_receipt_submit(doc, method=None):
    return None


def on_stock_entry_submit(doc, method=None):
    return None


def on_delivery_note_submit(doc, method=None):
    return None
