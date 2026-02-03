import frappe
from frappe import _
from frappe.utils import date_diff


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Maintenance ID"), "fieldname": "name", "fieldtype": "Link", "options": "Property Maintenance", "width": 120},
        {"label": _("Property"), "fieldname": "property", "fieldtype": "Link", "options": "Utility Property", "width": 120},
        {"label": _("Type"), "fieldname": "maintenance_type", "width": 100},
        {"label": _("Status"), "fieldname": "status", "width": 100},
        {"label": _("Reported"), "fieldname": "reported_date", "fieldtype": "Datetime", "width": 150},
        {"label": _("Completed"), "fieldname": "completion_date", "fieldtype": "Date", "width": 120},
        {"label": _("Response Time (Days)"), "fieldname": "response_time", "fieldtype": "Float", "width": 150}
    ]

def get_data(filters):
    maintenance_list = frappe.get_all("Property Maintenance", fields=["name", "property", "maintenance_type", "status", "reported_date", "completion_date"])

    data = []
    for m in maintenance_list:
        response_time = None
        if m.reported_date and m.completion_date:
            response_time = date_diff(m.completion_date, m.reported_date)

        data.append({
            "name": m.name,
            "property": m.property,
            "maintenance_type": m.maintenance_type,
            "status": m.status,
            "reported_date": m.reported_date,
            "completion_date": m.completion_date,
            "response_time": response_time
        })
    return data
