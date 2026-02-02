import frappe
from frappe.model.document import Document
from frappe.utils import nowdate


class PropertyMaintenance(Document):
    def validate(self):
        if self.status == "Completed" and not self.completion_date:
            self.completion_date = nowdate()

    def on_submit(self):
        if self.property and self.status == "In Progress":
            frappe.db.set_value("Utility Property", self.property, "status", "Under Maintenance")
        elif self.property and self.status == "Completed":
            # Check if property was under maintenance and set it back to available or occupied
            # For simplicity, we just clear the status if it was under maintenance
            current_status = frappe.db.get_value("Utility Property", self.property, "status")
            if current_status == "Under Maintenance":
                frappe.db.set_value("Utility Property", self.property, "status", "Available")
