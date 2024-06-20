from __future__ import unicode_literals
import frappe
from frappe import utils
from frappe import throw, _

import sys
import time
from zk import ZK, const
from datetime import datetime, timedelta
# from frappe.frappe.utils import date_diff,add_months, today,getdate, add_days, flt, get_last_day
from frappe.utils import date_diff, add_months, today, getdate, add_days, flt, get_last_day
import calendar
# from frappe.frappe.utils.background_jobs import enqueue
from frappe.utils.background_jobs import enqueue
from requests import request
import json
from frappe.model.document import Document
# from frappe.frappe.model.document import Document

class AttendanceAdjustment(Document):
	def validate(self):
		# if self.date:
		# 	if getdate(self.date) < add_days(getdate(),-6):
		# 		frappe.throw("Six days older adjustment are not allowed.")
		# if self.type != "Short Leave":
		# 	return True
		for data in self.table_4:
			att = frappe.db.sql(""" select p.name, c.check_in_1, c.check_out_1 from `tabEmployee Attendance` p 
			JOIN `tabEmployee Attendance Table` c
					ON c.parent = p.name where c.date=%s and p.month=%s and p.employee=%s""",
					(self.date,self.month,data.employee_id), as_dict=1)
			att_hrs = 0
			adjust_hrs = 0
			flg = False
			
			
			if len(att) > 0:
				
				if att[0]['check_in_1'] and att[0]['check_out_1']:
					
					x = datetime.strptime(
							str(att[0]['check_in_1']), '%H:%M:%S').time()
					y = datetime.strptime(
						str(att[0]['check_out_1']), '%H:%M:%S').time()
					xh, xm, xs = str(x).split(":")
					yh, ym, ys = str(y).split(":")
				
					first_in_time = timedelta(hours=float(
						xh), minutes=float(xm), seconds=float(xs))
					first_out_time = timedelta(hours=float(
						yh), minutes=float(ym), seconds=float(ys))
					diff = str(first_out_time - first_in_time)
					if "day" in diff:
						diff = diff.split("day, ")[1].split(":")
						diff = timedelta(hours=float(diff[0]), minutes=float(
							diff[1]), seconds=float(diff[2]))
					else:
						diff = first_out_time - first_in_time
					att_hrs = round(
							flt((diff).total_seconds())/3600, 2)

					#adjustment
					x = datetime.strptime(
							str(data.check_in), '%H:%M:%S').time()
					y = datetime.strptime(
						str(data.check_out), '%H:%M:%S').time()
					xh, xm, xs = str(x).split(":")
					yh, ym, ys = str(y).split(":")
				
					first_in_time = timedelta(hours=float(
						xh), minutes=float(xm), seconds=float(xs))
					first_out_time = timedelta(hours=float(
						yh), minutes=float(ym), seconds=float(ys))
					diff = str(first_out_time - first_in_time)
					if "day" in diff:
						diff = diff.split("day, ")[1].split(":")
						diff = timedelta(hours=float(diff[0]), minutes=float(
							diff[1]), seconds=float(diff[2]))
					else:
						diff = first_out_time - first_in_time
					adjust_hrs = round(
							flt((diff).total_seconds())/3600, 2)
					time_diff = adjust_hrs - att_hrs
					
					if time_diff == 0.0:
						data.no_of_hours = 0.0
					elif time_diff > 0 and time_diff <=3:
						data.no_of_hours = 3
					# elif time_diff > 3 and time_diff <=6:
					# 	data.no_of_hours = 6
					else:
						frappe.throw("Limit Exceded {0}.".format(str(time_diff)))
					flg = True
					

				elif att[0]['check_in_1']:
					
					x = datetime.strptime(
							str(att[0]['check_in_1']), '%H:%M:%S').time()
					y = datetime.strptime(
						str(data.check_out), '%H:%M:%S').time()
					xh, xm, xs = str(x).split(":")
					yh, ym, ys = str(y).split(":")
				
					first_in_time = timedelta(hours=float(
						xh), minutes=float(xm), seconds=float(xs))
					first_out_time = timedelta(hours=float(
						yh), minutes=float(ym), seconds=float(ys))
					diff = str(first_out_time - first_in_time)
					if "day" in diff:
						diff = diff.split("day, ")[1].split(":")
						diff = timedelta(hours=float(diff[0]), minutes=float(
							diff[1]), seconds=float(diff[2]))
					else:
						diff = first_out_time - first_in_time
					att_hrs = round(
							flt((diff).total_seconds())/3600, 2)
					if att_hrs > 0 and att_hrs <=3:
						data.no_of_hours = 3
					# elif att_hrs > 3 and att_hrs <=6:
					# 	data.no_of_hours = 6
					else:
						frappe.throw("Adjustment Limit Exceded (2).")
					flg = True


				elif att[0]['check_out_1']:
					
					x = datetime.strptime(
							str(data.check_in), '%H:%M:%S').time()
					y = datetime.strptime(
						str(att[0]['check_out_1']), '%H:%M:%S').time()
					xh, xm, xs = str(x).split(":")
					yh, ym, ys = str(y).split(":")
				
					first_in_time = timedelta(hours=float(
						xh), minutes=float(xm), seconds=float(xs))
					first_out_time = timedelta(hours=float(
						yh), minutes=float(ym), seconds=float(ys))
					diff = str(first_out_time - first_in_time)
					if "day" in diff:
						diff = diff.split("day, ")[1].split(":")
						diff = timedelta(hours=float(diff[0]), minutes=float(
							diff[1]), seconds=float(diff[2]))
					else:
						diff = first_out_time - first_in_time
					att_hrs = round(
							flt((diff).total_seconds())/3600, 2)
					if att_hrs > 0 and att_hrs <=3:
						data.no_of_hours = 3
					# elif att_hrs > 2 and att_hrs <=4:
					# 	data.no_of_hours = 4
					else:
						frappe.throw("Adjustment Limit Exceded (3).")
					flg = True

				
			if not flg:
				#adjustment
				x = datetime.strptime(
						str(data.check_in), '%H:%M:%S').time()
				y = datetime.strptime(
					str(data.check_out), '%H:%M:%S').time()
				xh, xm, xs = str(x).split(":")
				yh, ym, ys = str(y).split(":")
			
				first_in_time = timedelta(hours=float(
					xh), minutes=float(xm), seconds=float(xs))
				first_out_time = timedelta(hours=float(
					yh), minutes=float(ym), seconds=float(ys))
				diff = str(first_out_time - first_in_time)
				if "day" in diff:
					diff = diff.split("day, ")[1].split(":")
					diff = timedelta(hours=float(diff[0]), minutes=float(
						diff[1]), seconds=float(diff[2]))
				else:
					diff = first_out_time - first_in_time
				adjust_hrs = round(
						flt((diff).total_seconds())/3600, 2)
				
				if adjust_hrs > 0 and adjust_hrs <=2:
					data.no_of_hours = 2
				elif adjust_hrs > 2 and adjust_hrs <=4:
					data.no_of_hours = 4
				else:
					frappe.throw("Adjustment Limit Exceded {0}.".format(str(adjust_hrs)))
				

			existing_hrs = frappe.db.sql(""" select sum(c.no_of_hours) as hrs
					   from `tabAttendance Adjustment` p JOIN `tabAttendance Adjustment CT` c
					   ON c.parent = p.name where p.month=%s and c.employee_id=%s and c.name!=%s and p.docstatus=1""",(self.month,data.employee_id,data.name),as_dict=1)
			exst_hrs = 0.0
			
			
			if not data.no_of_hours:
				data.no_of_hours = 0.0
			if len(existing_hrs) > 0:
				exst_hrs = float(existing_hrs[0]['hrs'] or 0)
			if (float(data.no_of_hours) + exst_hrs) > 6:
				frappe.throw("Adjustment Limit Exceded. Availed hours = {0} and new hours request = {1}".format(str(exst_hrs),str(data.no_of_hours)))
	
	@frappe.whitelist()
	def create_logs(self):
		for data in self.table_4:
			if data.check_in:
				if self.type != "Short Leave":
					doc1 = frappe.new_doc("Attendance Logs")
					doc1.biometric_id= frappe.db.get_value("Employee",data.employee_id,"biometric_id")
					doc1.attendance = "&lt;Attendance&gt;: "+doc1.biometric_id+" : "+str(self.date)+" "+str(data.check_in)+" (1, 1)"
					doc1.attendance_date= self.date
					doc1.attendance_time= data.check_in
					doc1.type = "Check In"
					doc1.save(ignore_permissions=True)
					doc1.get_employee_attendance()
				att = frappe.db.sql(""" select p.name from `tabEmployee Attendance` p JOIN `tabEmployee Attendance Table` c
				ON c.parent = p.name where c.date=%s and p.month=%s and p.employee=%s """,(self.date,self.month,data.employee_id), as_dict=1)
				if len(att) > 0:
					frappe.db.sql(""" update `tabEmployee Attendance Table` set type=%s where date=%s and parent=%s""",(self.type,self.date,att[0]['name']))
					frappe.db.commit()
			if data.check_out:
				if self.type != "Short Leave":
					doc1 = frappe.new_doc("Attendance Logs")
					doc1.biometric_id= frappe.db.get_value("Employee",data.employee_id,"biometric_id")
					doc1.attendance = "&lt;Attendance&gt;: "+doc1.biometric_id+" : "+str(self.date)+" "+str(data.check_out)+" (1, 1)"
					doc1.attendance_date= self.date
					doc1.attendance_time= data.check_out
					doc1.type = "Check Out"
					doc1.save(ignore_permissions=True)
					doc1.get_employee_attendance()
				att = frappe.db.sql(""" select p.name from `tabEmployee Attendance` p JOIN `tabEmployee Attendance Table` c
				ON c.parent = p.name where c.date=%s and p.month=%s and p.employee=%s """,(self.date,self.month,data.employee_id), as_dict=1)
				if len(att) > 0:
					frappe.db.sql(""" update `tabEmployee Attendance Table` set type=%s where date=%s and parent=%s""",(self.type,self.date,att[0]['name']))
					frappe.db.commit()
	def on_submit(self):
		pass


def adj_settle():
	docs = frappe.get_all("Attendance Adjustment",filters={"month":"March","workflow_state": "Approved"},fields=["name"])
	for rec in docs:
		doc = frappe.get_doc("Attendance Adjustment",rec.name)
		doc.create_logs()

@frappe.whitelist()
def test_func():
	enqueue(adj_settle, queue='short', timeout=5000)
	return "OK"
	

@frappe.whitelist()
def get_check_in_out(date=None, month=None, employee_id=None):
	att = frappe.db.sql(""" select p.name, c.check_in_1, c.check_out_1 from `tabEmployee Attendance` p 
			JOIN `tabEmployee Attendance Table` c
					ON c.parent = p.name where c.date=%s and p.month=%s and p.employee=%s""",
					(date, month, employee_id), as_dict=1)
	check_in="00:00:00"
	check_out="00:00:00"
	if len(att) > 0:
		if att[0]['check_in_1'] :
			check_in = att[0]['check_in_1']

		if att[0]['check_out_1']:
			check_out = att[0]['check_out_1']
	return [check_in, check_out]

