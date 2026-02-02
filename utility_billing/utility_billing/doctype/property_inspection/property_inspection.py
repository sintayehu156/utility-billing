import frappe
from frappe.model.document import Document


class PropertyInspection(Document):
    def on_submit(self):
        if self.property:
            frappe.db.set_value("Utility Property", self.property, "latest_inspection", self.name)

            # If move-out inspection is completed, optionally set property to available
            if self.inspection_type == "Move-out":
                frappe.db.set_value("Utility Property", self.property, "status", "Available")
