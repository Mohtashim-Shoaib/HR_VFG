# Copyright (c) 2024, VFG and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OvertimeForm(Document):
	@frappe.whitelist()
	def get_data(self):
		rec = frappe.db.sql(""" select p.employee,p.employee_name, p.designation, c.late_sitting,c.approved_ot1, c.name as child_name, p.name as parent_name from `tabEmployee Attendance` p
					  LEFT JOIN `tabEmployee Attendance Table` c ON c.parent=p.name
					  where p.month=%s and p.year=%s and c.date=%s and c.late_sitting is not  NULL""",
					  (self.month,self.year,self.date),as_dict=1)
		
		if len(rec) > 0:
			self.details = []
		for r in rec:
			allow_ot = frappe.db.get_value('Employee', r.employee, 'is_overtime_allowed')
			if allow_ot == 1 and r.approved_ot1 == "00:00:00" and r.late_sitting:
				self.append("details",{
					"employee":r.employee,
					"actual_overtime":r.late_sitting,
					"approved_overtime":r.late_sitting,
					"employee_name":r.employee_name,
					"designation":r.designation,
					"att_ref":r.parent_name,
					"att_child_ref":r.child_name
				})
		self.save()

	def on_submit(self):
		for r in self.details:
			frappe.db.sql("update `tabEmployee Attendance Table` set approved_ot1=%s where name=%s",(r.approved_overtime,r.att_child_ref))
			frappe.db.commit()
			doc = frappe.get_doc("Employee Attendance",r.att_ref)
			doc.save()


	

