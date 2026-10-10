# gcn_jewelry

ERPNext/Frappe custom application for stainless-steel jewelry operations.

This package is isolated from ERPNext core. It adds the business model, cargo timeline, replenishment calculations, and Feishu read-only synchronization.

## Scope

- Standard ERPNext documents remain the source of truth for items, warehouses, suppliers, purchase orders, receipts, stock entries, work orders, job cards, delivery notes, and sales orders.
- Custom DocTypes cover SKU profiles, production stages, procurement batches, replenishment rules and anomalies, Feishu sync records/logs, and shipment tracking.
- Cargo stages are normalized into one timeline: 采购/买胚 → 做胚/定做 → 溜光 → 抛光 → 烧焊 → 电抛 → 电镀 → 镶钻/粘钻 → 清洗/手工 → 质检 → 入库 → 发货.
- Feishu synchronization is read-only by default. It records source table/row IDs and never creates purchase orders or stock movements during the pilot.

## Install

From a Frappe bench, install this app alongside ERPNext:

~~~bash
bench get-app gcn_jewelry <repository-url> --branch gcn-jewelry-custom-app
bench --site <site-name> install-app gcn_jewelry
bench --site <site-name> migrate
~~~

The Feishu credentials belong in site config or a secret manager, never in Git. Complete the read-only reconciliation before enabling write-back.
