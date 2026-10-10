import frappe


@frappe.whitelist()
def sync_full():
    return frappe.enqueue(
        "gcn_jewelry.integrations.feishu.sync.sync_full",
        queue="long",
        job_name="gcn_jewelry-feishu-full",
    )


@frappe.whitelist()
def sync_incremental():
    return frappe.enqueue(
        "gcn_jewelry.integrations.feishu.sync.sync_incremental",
        queue="long",
        job_name="gcn_jewelry-feishu-incremental",
    )
