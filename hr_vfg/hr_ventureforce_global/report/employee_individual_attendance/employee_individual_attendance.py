# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from multiprocessing import Condition
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe import msgprint, _
from datetime import datetime
from datetime import timedelta
from datetime import date as dt
import datetime as special
import time
# from hrms.hr.utils import get_holidays_for_employee
from hrms.hrms.hr.utils import get_holidays_for_employee
from frappe.utils import date_diff, add_months, today, getdate, add_days, flt, get_last_day
import calendar

def execute(filters=None):
	columns, data = [], []
	return get_columns(), get_data(filters)

def get_data(filters):
	condition = {
		"month":filters.get("month",None)
	}
	if filters.get("depart", None):
		condition["department"]=filters.depart
	if filters.get("employee", None):
		condition["employee"]=filters.employee
	res = frappe.db.get_all("Employee Attendance", filters = condition,fields=["name"])
	data =[]
	for d in res:
			doc = frappe.get_doc("Employee Attendance", d.name)
			
			for item in doc.table1:
				#lv = frappe.get_all("Leave Application", filters={"from_date":["<=",getdate(item.date)],"to_date":[">=",getdate(item.date)],"employee":doc.employee,"status":"Approved"},fields=["*"])
				shift_req = frappe.get_all("Shift Request", filters={'employee': doc.employee,
																			'from_date': ["<=", item.date], 'to_date': [">=", item.date]}, fields=["*"])
				shift = None
				if len(shift_req) > 0:
					shift = shift_req[0].shift_type
				else:
					shift_ass = frappe.get_all("Shift Assignment", filters={'employee': doc.employee,
																			'date': ["<=", item.date]}, fields=["*"])
					if len(shift_ass) > 0:
						shift = shift_ass[0].shift_type
				if shift == None:
					shift_doc = None
							
				else:
					shift_doc = frappe.get_doc("Shift Type", shift)
				
				
				
				day_name = datetime.strptime(
					str(item.date), '%Y-%m-%d').strftime('%A')

				day_data=None
				if shift_doc:
						for day in shift_doc.days:
							if day_name == day.day:
								day_data = day
								break
				if not day_data:
					if item.check_in_1 and item.check_out_1:
						schedule_time_in = "00:00:00"
						schedule_time_out = "00:00:00"
					else:
						continue
				else:
					schedule_time_in = day_data.start_time
					schedule_time_out = day_data.end_time
				att_status = "In Time"
				if item.late:
					att_status = "Late Entry"
				elif item.absent:
					att_status = "Absent"
				elif item.half_day:
					att_status = "Half Day"
				if item.sunday or item.holiday:
					att_status = "Off"
				if item.type:
					att_status = item.type
				if att_status == "Absent":
								leaves  = frappe.get_all("Leave Application", filters={'employee': doc.employee,
																						'from_date': ["<=", item.date], 'to_date': [">=", item.date],"status":"Approved"}, fields=["*"])
								if len(leaves) > 0:
									att_status = leaves[0].leave_type
				row={
					"emp_id":doc.employee,
					"name":doc.employee_name,
					"department":doc.department,
					"designation":frappe.db.get_value("Employee",{"name":doc.employee},"designation"),
					"date":getdate(item.date),
					"day":day_name[:3],
					"schedule_time_in":schedule_time_in,
					"actual_in_time":item.check_in_1,
					"schedule_time_out":schedule_time_out,
					"actual_out_time":item.check_out_1,
					"late_arrival":round(flt((datetime.strptime( item.late_coming_hours, "%H:%M:%S").hour *60)+(datetime.strptime( item.late_coming_hours, "%H:%M:%S").minute)+(datetime.strptime( item.late_coming_hours, "%H:%M:%S").second/60)), 2)if item.late and item.late_coming_hours else "00",
					"early_going":round(flt((datetime.strptime( item.early_going_hours, "%H:%M:%S").hour *60)+(datetime.strptime( item.early_going_hours, "%H:%M:%S").minute)+(datetime.strptime( item.early_going_hours, "%H:%M:%S").second/60)), 2)if item.early and item.early_going_hours else "00",
					"work_hours":item.per_day_hour,
					"total_hours":item.difference,
					"overtime":item.late_sitting,
					"day_status":"Holiday" if item.sunday or item.holiday else "Working Day",
					"att_status":att_status
				}
				data.append(row)

			data.append({
				"name":"<h4>Summary</h4>"
			})
			data.append({
				"name":"<b>Hours Worked</b>",
				"department":doc.hours_worked,

				"designation":"<b>Present Days</b>",
				"date":doc.present_days,

				"day":"<b>Late Sitting Hrs</b>",
				"schedule_time_in":doc.late_sitting_hours,


			})
		
			data.append({
				"name":"<b>Over Time (Hrs)</b>",
				"department":doc.over_time,

				"designation":"<b>Short Hours</b>",
				"date":doc.short_hours,

				"day":"<b>Total Absents</b>",
				"schedule_time_in":doc.total_absents
			})
			
			data.append({
				"name":"<b>Half Days</b>",
				"department":doc.total_half_days,

				"designation":"<b>Total :Lates</b>",
				"date":doc.total_lates,

				"day":"<b>Total Early Goings</b>",
				"schedule_time_in":doc.total_early_goings
			})
			data.append(["<hr>","<hr>","<hr>","<hr>","<hr>","<hr>","<hr>","<hr>","<hr>","<hr>","<hr>","<hr>","<hr>","<hr>","<hr>","<hr>","<hr>",])

			
	return data

def get_columns():
	columns=[
		{
			"label": _("EMP #"),
			"fieldname": "emp_id",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 120
		},
		{
			"label": _("Name"),
			"fieldname": "name",
			"fieldtype": "Data",
			"width": 220
		},
		{
			"label": _("department"),
			"fieldname": "department",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Designation"),
			"fieldname": "designation",
			"fieldtype": "Data",
			"width": 200
		},
		
		{
			"label": _("Date"),
			"fieldname": "date",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Day"),
			"fieldname": "day",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Sch In Time"),
			"fieldname": "schedule_time_in",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Act In Time"),
			"fieldname": "actual_in_time",
			"fieldtype": "Data",
			"width": 120
		},

		{
			"label": _("Sch Out Time"),
			"fieldname": "schedule_time_out",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Act Out Time"),
			"fieldname": "actual_out_time",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Late Arrival (Min)"),
			"fieldname": "late_arrival",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Day Status"),
			"fieldname": "day_status",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Att Status"),
			"fieldname": "att_status",
			"fieldtype": "Data",
			"width": 120
		},

		{
			"label": _("Work Hours"),
			"fieldname": "work_hours",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Total Hours"),
			"fieldname": "total_hours",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Overtime"),
			"fieldname": "overtime",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Leave Early (Min)"),
			"fieldname": "early_going",
			"fieldtype": "Data",
			"width": 120
		},

	]
	return columns