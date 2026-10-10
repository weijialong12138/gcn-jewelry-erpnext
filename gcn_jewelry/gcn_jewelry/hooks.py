app_name = "gcn_jewelry"
app_title = "GCN Jewelry"
app_publisher = "GCN Jewelry"
app_description = "Jewelry production, replenishment and Feishu integration extensions"
app_email = "ops@gcn-jewelry.local"
app_license = "MIT"
required_apps = ["erpnext"]

doc_events = {
    "Purchase Order": {
        "on_update": "gcn_jewelry.services.replenishment.on_purchase_order_update",
    },
    "Purchase Receipt": {
        "on_submit": "gcn_jewelry.services.replenishment.on_purchase_receipt_submit",
    },
    "Stock Entry": {
        "on_submit": "gcn_jewelry.services.replenishment.on_stock_entry_submit",
    },
    "Work Order": {
        "on_update": "gcn_jewelry.services.cargo.on_work_order_update",
    },
    "Delivery Note": {
        "on_submit": "gcn_jewelry.services.replenishment.on_delivery_note_submit",
    },
}

scheduler_events = {
    "hourly": [
        "gcn_jewelry.services.cargo.scan_stage_timeouts",
    ],
    "daily": [
        "gcn_jewelry.services.replenishment.scan_replenishment_anomalies",
        "gcn_jewelry.integrations.feishu.sync.enqueue_incremental",
    ],
}

doctype_js = {
    "Purchase Order": "public/js/purchase_order.js",
    "Purchase Receipt": "public/js/purchase_receipt.js",
    "Stock Entry": "public/js/stock_entry.js",
}

app_include_js = ["/assets/gcn_jewelry/js/gcn_jewelry.js"]
