import frappe
from frappe import _
from frappe.utils import date_diff, today


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Invoice"), "fieldname": "name", "fieldtype": "Link", "options": "Sales Invoice", "width": 120},
        {"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 120},
        {"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 100},
        {"label": _("Days Overdue"), "fieldname": "days_overdue", "fieldtype": "Int", "width": 100},
        {"label": _("Outstanding Amount"), "fieldname": "outstanding_amount", "fieldtype": "Currency", "options": "currency", "width": 120},
        {"label": _("Eligible for Termination"), "fieldname": "termination_eligible", "fieldtype": "Check", "width": 150}
    ]

def get_data(filters):
    invoices = frappe.get_all("Sales Invoice", filters={
        "docstatus": 1,
        "status": "Overdue",
        "outstanding_amount": [">", 0]
    }, fields=["name", "customer", "due_date", "outstanding_amount", "currency"])

    data = []
    for inv in invoices:
        days_overdue = date_diff(today(), inv.due_date)
        data.append({
            "name": inv.name,
            "customer": inv.customer,
            "due_date": inv.due_date,
            "days_overdue": days_overdue,
            "outstanding_amount": inv.outstanding_amount,
            "currency": inv.currency,
            "termination_eligible": 1 if days_overdue >= 30 else 0
        })
    return data
