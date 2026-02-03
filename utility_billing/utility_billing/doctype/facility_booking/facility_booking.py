import frappe
from frappe import _
from frappe.model.document import Document


class FacilityBooking(Document):
    def validate(self):
        self.validate_overlap()

    def validate_overlap(self):
        if not (self.facility_type and self.booking_date and self.start_time and self.end_time):
            return

        overlap = frappe.db.sql("""
            SELECT name FROM `tabFacility Booking`
            WHERE facility_type = %s
              AND booking_date = %s
              AND name != %s
              AND docstatus < 2
              AND (
                (start_time <= %s AND end_time > %s) OR
                (start_time < %s AND end_time >= %s) OR
                (start_time >= %s AND start_time < %s)
              )
        """, (
            self.facility_type, self.booking_date, self.name or "NEW",
            self.start_time, self.start_time,
            self.end_time, self.end_time,
            self.start_time, self.end_time
        ))

        if overlap:
            frappe.throw(_("The {0} is already booked for this time slot on {1} ({2})").format(
                self.facility_type, self.booking_date, overlap[0][0]
            ))
