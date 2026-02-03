// Copyright (c) 2025, Navari and contributors
// For license information, please see license.txt

frappe.ui.form.on("Contract", {
	refresh: function (frm) {
		frm.fields_dict.properties.grid.cannot_add_rows = true;
		frm.fields_dict["properties"].grid.get_field("utility_property").get_query = function () {
			return {
				filters: {
					status: "Available",
				},
			};
		};

		set_is_active_readonly(frm);

		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(
				__("Log Communication"),
				function () {
					frappe.model.with_doctype("PMS Communication Log", function () {
						let new_doc = frappe.model.get_new_doc("PMS Communication Log");
						new_doc.reference_doctype = frm.doc.doctype;
						new_doc.reference_name = frm.doc.name;
						new_doc.recipient = frm.doc.party_name;
						frappe.set_route("Form", "PMS Communication Log", new_doc.name);
					});
				},
				__("Actions")
			);

			frm.add_custom_button(
				__("Create Inspection"),
				function () {
					frappe.model.with_doctype("Property Inspection", function () {
						let new_doc = frappe.model.get_new_doc("Property Inspection");
						new_doc.tenant = frm.doc.party_name;
						if (frm.doc.properties && frm.doc.properties.length > 0) {
							new_doc.property = frm.doc.properties[0].utility_property;
						}
						frappe.set_route("Form", "Property Inspection", new_doc.name);
					});
				},
				__("Actions")
			);
		}
	},
});

frappe.ui.form.on("Contract Utility Property Item", {
	is_active: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (frm.doc.docstatus === 1 && !row.__islocal && row.is_active) {
			frappe.msgprint("You cannot activate a property once the contract is submitted.");
			frappe.model.set_value(cdt, cdn, "is_active", 0);
		}
	},

	form_render: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (frm.doc.docstatus === 1 && !row.is_active) {
			frm.fields_dict.properties.grid.grid_rows_by_docname[cdn].toggle_editable(
				"is_active",
				false
			);
		} else {
			frm.fields_dict.properties.grid.grid_rows_by_docname[cdn].toggle_editable(
				"is_active",
				true
			);
		}
	},
});

function set_is_active_readonly(frm) {
	if (frm.doc.docstatus === 1) {
		(frm.doc.properties || []).forEach((row) => {
			let grid_row = frm.fields_dict.properties.grid.grid_rows_by_docname[row.name];
			if (grid_row) {
				grid_row.toggle_editable("is_active", row.is_active ? true : false);
			}
		});
	}
}
