# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeShiftTransfer(Document):	
	def on_submit(self):
		self.create_shift_transfers()
	def create_shift_transfers(self):
		for row in self.select_employee:
			shift = frappe.db.get_value('Shift Assignment', {'employee': row.employee_name,'status':'Active','docstatus':1}, ['name'])
			if shift:
				doc = frappe.get_doc("Shift Assignment",shift)
				doc.status = "Inactive"
				doc.save()
				shift_ass = frappe.new_doc('Shift Assignment')
				shift_ass.employee = row.employee_name
				shift_ass.department = self.department
				shift_ass.shift_type = self.shift_type
				shift_ass.start_date = self.shift_date
				shift_ass.save()
				shift_ass.submit()
				emp = frappe.get_doc("Employee", row.employee_name)
				emp.default_shift = self.shift_type
				emp.save()
			if not shift:
				shift_ass = frappe.new_doc('Shift Assignment')
				shift_ass.employee = row.employee_name
				shift_ass.department = self.department
				shift_ass.shift_type = self.shift_type
				shift_ass.start_date = self.shift_date
				shift_ass.save()
				shift_ass.submit()
				emp = frappe.get_doc("Employee", row.employee_name)
				emp.default_shift = self.shift_type
				emp.save()