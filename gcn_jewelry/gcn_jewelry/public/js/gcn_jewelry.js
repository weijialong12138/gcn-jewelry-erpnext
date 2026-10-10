frappe.provide("gcn_jewelry");

gcn_jewelry.get_status_badge = function (status) {
    const colors = {
        Open: "orange",
        "In Progress": "blue",
        Completed: "green",
        Overdue: "red",
    };
    return colors[status] || "grey";
};
