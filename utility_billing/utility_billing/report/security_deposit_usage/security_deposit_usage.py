import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Contract"), "fieldname": "name", "fieldtype": "Link", "options": "Contract", "width": 150},
        {"label": _("Tenant"), "fieldname": "party_name", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": _("Security Deposit Amount"), "fieldname": "security_deposit_amount", "fieldtype": "Currency", "width": 150},
        {"label": _("Deposit Received"), "fieldname": "security_deposit_received", "fieldtype": "Check", "width": 120}
    ]

def get_data(filters):
    contracts = frappe.get_all("Contract", filters={
        "docstatus": 1
    }, fields=["name", "party_name", "security_deposit_amount", "security_deposit_received"])

    return contracts
