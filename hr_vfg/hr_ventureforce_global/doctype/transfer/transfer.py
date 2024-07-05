# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe.utils import flt, getdate

from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
from hrms.hr.utils import set_employee_name
import copy
import json
import datetime

import frappe
from frappe import _, msgprint
from frappe.model.document import Document
from frappe.utils import (
	add_days,
	ceil,
	cint,
	comma_and,
	flt,
	get_link_to_form,
	getdate,
	now_datetime,
	nowdate,
)
from frappe.utils.csvutils import build_csv_response
from six import iteritems

from erpnext.manufacturing.doctype.bom.bom import get_children, validate_bom_no
from erpnext.manufacturing.doctype.work_order.work_order import get_item_details
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults

class Transfer(Document):
	pass
	def before_submit(self):
		self.set_employee_form()
	def set_employee_form(self):
		emp = frappe.get_doc("Employee", self.employee)
		emp.department = self.new_department
		emp.designation = self.designation_name
		emp.file_no = self.new_file_no
		emp.salary = self.current_salary
		emp.conveyance_allowance = self.current_allowance
		emp.medical_allowance = self.current_medical
		emp.save()
		if self.shift:
			shift = frappe.get_last_doc('Shift Assignment', filters={"employee": self.employee})
			if shift:
				shift.cancel()
				shift.delete()
				new_shift = frappe.new_doc("Shift Assignment")
				new_shift.employee = self.employee
				new_shift.shift_type = self.shift
				new_shift.date = self.date_2
				new_shift.save()
				new_shift.submit()
		if self.salary_increment > 0:
			assign = frappe.get_last_doc('Salary Structure Assignment', filters={"employee": self.employee})
			assign.base = self.current_salary
			assign.save()