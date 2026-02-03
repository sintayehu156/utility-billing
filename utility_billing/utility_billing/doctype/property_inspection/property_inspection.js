frappe.ui.form.on("Property Inspection", {
	property: function (frm) {
		if (frm.doc.property && (!frm.doc.items || frm.doc.items.length === 0)) {
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Utility Property",
					name: frm.doc.property,
				},
				callback: function (r) {
					if (r.message && r.message.inventory) {
						frm.clear_table("items");
						r.message.inventory.forEach((item) => {
							let row = frm.add_child("items");
							row.item_name = item.item_name;
							row.condition = item.base_condition;
							row.remarks = item.description;
						});
						frm.refresh_field("items");
					}
				},
			});
		}
	},
});
