# Copyright (c) 2025, Navari Ltd and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    summary = get_report_summary(data)
    chart = get_chart_data(data)
    return columns, data, None, chart, summary


def get_columns():
	return [
		{"label": "Property", "fieldname": "property_name", "fieldtype": "Link", "options": "Utility Property", "width": 200},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": "Location", "fieldname": "location", "fieldtype": "Link", "options": "Location", "width": 180},
		{"label": "Utility Category", "fieldname": "utility_category", "fieldtype": "Link", "options": "Utility Category", "width": 150},
		{"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
		{"label": "Is Fixed Asset", "fieldname": "is_fixed_asset", "fieldtype": "Check", "width": 100},
		{"label": "Gross Purchase Amount", "fieldname": "gross_purchase_amount", "fieldtype": "Currency", "width": 140},
		{"label": "Unit Number", "fieldname": "unit_number", "fieldtype": "Data", "width": 120},
		{"label": "Bedrooms", "fieldname": "bedrooms", "fieldtype": "Int", "width": 100},
		{"label": "Bathrooms", "fieldname": "bathrooms", "fieldtype": "Int", "width": 100},
		{"label": "Unit Size (sqft)", "fieldname": "unit_size", "fieldtype": "Float", "width": 120},
		{"label": "Floor Level", "fieldname": "floor_level", "fieldtype": "Link", "options": "Floor Level", "width": 120},
	]

def get_data(filters):
    filters = filters or {}
    conditions = {"is_group": 0}


    exact_filters = ["status", "utility_category", "company", "is_fixed_asset"]
    for key in exact_filters:
        if key in filters and filters[key] not in [None, ""]:
            conditions[key] = filters[key]


    if filters.get("location"):
        conditions["location"] = ["like", f"%{filters['location']}%"]


    range_fields = ["bedrooms", "bathrooms", "unit_size"]
    for field in range_fields:
        min_val = filters.get(f"min_{field}")
        max_val = filters.get(f"max_{field}")

        if min_val not in [None, ""] and max_val not in [None, ""]:
            conditions[field] = ["between", [min_val, max_val]]
        elif min_val not in [None, ""]:
            conditions[field] = [">=", min_val]
        elif max_val not in [None, ""]:
            conditions[field] = ["<=", max_val]

    props = frappe.get_all(
        "Utility Property",
        filters=conditions,
        fields=[
            "property_name", "status", "location", "utility_category", "company",
            "is_fixed_asset", "gross_purchase_amount", "unit_number",
            "bedrooms", "bathrooms", "unit_size", "floor_level", "modified"
        ]
    )
    return props


def get_report_summary(data):
    total_properties = len(data)
    total_value = sum(d.get("gross_purchase_amount", 0) or 0 for d in data)
    available_units = sum(1 for d in data if d.get("status") == "Available")

    currency = None
    if data:
        currency = frappe.get_cached_value("Company", data[0].get("company"), "default_currency")

    return [
        {"label": "Total Properties", "value": total_properties, "indicator": "blue"},
        {"label": "Available Units", "value": available_units, "indicator": "green"},
        {
            "label": "Total Asset Value",
            "value": total_value,
            "indicator": "orange",
            "datatype": "Currency",
            "currency": currency,
        },
    ]

def get_chart_data(data):
    status_counts = {}
    for d in data:
        status = d.get("status") or "No Status"
        status_counts[status] = status_counts.get(status, 0) + 1

    labels = list(status_counts.keys())
    values = list(status_counts.values())

    color_map = {
        "Available": "green",
        "Occupied": "blue",
        "Under Maintenance": "orange",
        "Reserved": "purple",
    }

    colors = [color_map.get(label, "#808080") for label in labels]

    return {
        "data": {
            "labels": labels,
            "datasets": [{
                "name": "Properties",
                "values": values
            }]
        },
        "type": "pie",
        "colors": colors
    }
