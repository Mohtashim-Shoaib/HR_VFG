# -*- coding: utf-8 -*-
# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint, _
from datetime import datetime
from datetime import timedelta
from datetime import date as dt
import datetime as special
import time
from hrms.hr.utils import get_holidays_for_employee
from frappe.utils import cstr, flt,getdate, today
import calendar


class OverTime(Document):
	def validate(self):
		checkOut= timedelta(hours=0,minutes=0, seconds=0)
		adjusted = timedelta(hours=0,minutes=0, seconds=0)
		for d in self.table_4:
			if d.actual_over_time and d.adjusted_over_time:
				x = datetime.strptime(
						str(d.actual_over_time), '%H:%M:%S').time()
					
				xh, xm, xs = str(x).split(":")
							
				aot = timedelta(hours=float(
									xh), minutes=float(xm), seconds=float(xs))

				x = datetime.strptime(
						str(d.adjusted_over_time), '%H:%M:%S').time()
					
				xh, xm, xs = str(x).split(":")
							
				adot = timedelta(hours=float(
									xh), minutes=float(xm), seconds=float(xs))
				if (aot < adot):
					frappe.throw("Approved Over time is greater than actual.")
			x = datetime.strptime(
						str(d.actual_over_time), '%H:%M:%S').time()
				
			xh, xm, xs = str(x).split(":")
						
			ot = timedelta(hours=float(
								xh), minutes=float(xm), seconds=float(xs))
			checkOut+=ot
			
			if d.adjusted_over_time:
				x = datetime.strptime(
						str(d.adjusted_over_time), '%H:%M:%S').time()
					
				xh, xm, xs = str(x).split(":")
							
				ot = timedelta(hours=float(
									xh), minutes=float(xm), seconds=float(xs))
				adjusted+= ot

		self.total_actual_over_time = round(
									  flt(checkOut.total_seconds())/3600, 2)
		self.total_adjusted_over_time = round(
									  flt(adjusted.total_seconds())/3600, 2)
		atdoc = frappe.db.get_value('Employee Attendance', {'employee': self.data_8,'month':self.month}, ['name'])
		epa = frappe.get_doc("Employee Attendance",atdoc)
		epa.total_adjusted_over_time = self.total_adjusted_over_time
		epa.save()
	def on_submit(self):
		for d in self.table_4:
			result  = frappe.db.sql(""" select c.late_sitting,p.name as empa, c.name,c.approved_ot1 from `tabEmployee Attendance` p
										JOIN `tabEmployee Attendance Table` c ON c.parent=p.name
										where p.employee=%s and p.month=%s and c.date=%s""",
										(self.data_8,self.month,d.date),
										as_dict=1)
				
			if len(result) > 0:
				x = datetime.strptime(
						str(d.adjusted_over_time), '%H:%M:%S').time()
					
				xh, xm, xs = str(x).split(":")
							
				adot = timedelta(hours=float(
									xh), minutes=float(xm), seconds=float(xs))
				frappe.db.sql(""" update `tabEmployee Attendance Table` set approved_ot1=%s where name=%s""",
							( adot,result[0]["name"]))
				frappe.db.commit()
				doc = frappe.get_doc("Employee Attendance",result[0]['empa'])
				doc.save()
	
	def on_cancel(self):
		for d in self.table_4:
			result  = frappe.db.sql(""" select c.late_sitting,p.name as empa, c.name,c.approved_ot1 from `tabEmployee Attendance` p
										JOIN `tabEmployee Attendance Table` c ON c.parent=p.name
										where p.employee=%s and p.month=%s and c.date=%s""",
										(self.data_8,self.month,d.date),
										as_dict=1)
				
			if len(result) > 0:
				frappe.db.sql(""" update `tabEmployee Attendance Table` set approved_ot1=%s where name=%s""",
							(0.0,result[0]["name"]))
				frappe.db.commit()
				doc = frappe.get_doc("Employee Attendance",result[0]['empa'])
				doc.save()
	
	@frappe.whitelist()
	def get_overtime(self,employee,month):
			result  = frappe.db.sql(""" select c.check_in_1, c.check_out_1, c.late_sitting,c.date, c.name,c.approved_ot1 from `tabEmployee Attendance` p
									JOIN `tabEmployee Attendance Table` c ON c.parent=p.name
									where p.employee=%s and p.month=%s and c.late_sitting is not NULL""",
									(employee,month),
									as_dict=1)
			
			data = []
			if len(result) > 0:
				for d in result:
					ot_hrs = 0.0
					# if d.late_sitting:
					# 	x = datetime.strptime(
					# 				str(d.late_sitting), '%H:%M:%S').time()
							
					# 	xh, xm, xs = str(x).split(":")
									
					# 	ot = timedelta(hours=float(
					# 					xh), minutes=float(xm), seconds=float(xs))
					# 	ot_hrs = round(
					# 				flt(ot.total_seconds())/3600, 2)
					
					data.append({
						"date":d.date,
						"actual_over_time":d.late_sitting,
						"checkin":d.check_in_1,
						"checkout":d.check_out_1
					})
				return data
			else:
				frappe.msgprint("No record found")
			return data