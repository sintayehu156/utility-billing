import frappe
from frappe import _
from frappe.model.document import Document


class UnitSwapRequest(Document):
    def on_submit(self):
        if self.status != "Approved":
            frappe.throw(_("Status must be 'Approved' to execute the swap on submission."))

        self.execute_swap()

    def execute_swap(self):
        # 1. Update historical records / Log
        frappe.msgprint(_("Executing unit swap from {0} to {1} for tenant {2}").format(
            self.current_property, self.target_property, self.tenant
        ))

        # 2. Update active contracts
        contracts = frappe.get_all("Contract", filters={
            "party_name": self.tenant,
            "status": "Active",
            "docstatus": 1
        }, fields=["name"])

        updated_contracts = 0
        for c in contracts:
            contract_doc = frappe.get_doc("Contract", c.name)
            for prop in contract_doc.properties:
                if prop.utility_property == self.current_property and prop.is_active:
                    prop.utility_property = self.target_property
                    updated_contracts += 1
            contract_doc.save(ignore_permissions=True)

        # 3. Update property statuses
        frappe.db.set_value("Utility Property", self.current_property, "status", "Available")
        frappe.db.set_value("Utility Property", self.target_property, "status", "Occupied")

        self.db_set("status", "Executed")

        frappe.msgprint(_("Successfully updated {0} contracts and property statuses.").format(updated_contracts))
