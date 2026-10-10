CARGO_FIELD_MAP = {
    "款式名称": "sku_name",
    "商品名称": "sku_name",
    "SKU": "sku",
    "订单数量": "order_qty",
    "当前状态": "current_status",
    "生产中状态跟进": "stage_note",
    "客户要求交期": "customer_due_date",
    "客户名称": "customer",
    "采购编号": "procurement_batch",
    "备注": "remarks",
}

INVENTORY_FIELD_MAP = {
    "商品编号/SKU": "sku",
    "商品名称": "sku_name",
    "初始库存": "opening_stock",
    "当前累计出库数量": "issued_qty",
    "库位号": "warehouse_location",
    "当前成本价值": "stock_value",
    "备注": "remarks",
}


def map_fields(fields: dict, field_map: dict) -> dict:
    return {
        target: fields[source]
        for source, target in field_map.items()
        if source in fields and fields[source] not in (None, "")
    }
