# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
# from frappe.utils import flt, getdate, add_months, get_last_day, fmt_money, nowdate,cstr, cint

# from frappe import msgprint, _
# from calendar import monthrange

# day_abbr = [
# 		"Mon",
# 		"Tue",
# 		"Wed",
# 		"Thu",
# 		"Fri",
# 		"Sat",
# 		"Sun"
# 	]
# month_list = ['January','February','March','April','May','June','July','August','September',
# 		'October','November','December']


# def execute(filters=None):
# 	columns, data = [], []
# 	columns = get_columns(filters)
# 	data  = get_data(filters)
# 	return columns, data

# def get_columns(filters):
# 	columns =  [
		
# 		{
# 			"fieldtype":"Link",
# 			"fieldname":"department",
# 			"options":"Department",
# 			"label":"Department",
# 			"width":200,
# 		},

# 		{
# 			"fieldtype":"Int",
# 			"fieldname":"total_employee",
# 			"label":"Total Employee",
# 			"width":200,
# 		},
# 		{
# 			"fieldtype":"Int",
# 			"fieldname":"on_time",
# 			"label":"On Time",
# 			"width":200,
# 		},
# 		{
# 			"fieldtype":"Int",
# 			"fieldname":"late_present",
# 			"label":"Late Present",
# 			"width":200,
# 		},
# 		{
# 			"fieldtype":"Int",
# 			"fieldname":"total_present",
# 			"label":"Total Present",
# 			"width":200,
# 		},
# 		{
# 			"fieldtype":"Int",
# 			"fieldname":"total_absent",
# 			"label":"Total Absent",
# 			"width":200,
# 		},
# 	]

# 	return columns
# def get_data(filters):
# 	data = []
# 	rec = frappe.db.sql(""" 
# 	           select p.department, c.late, c.early, c.sunday,c.holiday,c.absent ,c.half_day
# 			   from `tabEmployee Attendance` p
# 			   LEFT JOIN 
# 			   `tabEmployee Attendance Table` c
# 			   on c.parent = p.name
# 			   where c.date = %s 
# 	 """,(filters.to_date),as_dict=1)
# 	for r in rec:
# 		exists = False
# 		for d in data:
# 			if r.get("department") == d.get("department"):
# 				d["total_employee"] =  d["total_employee"]+1
# 				if r.get("absent"):
# 					d["total_absent"] =  d["total_absent"]+1
# 				elif r.get("sunday") or r.get("holiday"):
# 					pass
# 				elif r.get("late"):
# 					d["late_present"] =  d["late_present"]+1
# 					d["total_present"] =  d["total_present"]+1
# 				else:
# 					d["on_time"] =  d["on_time"]+1
# 					d["total_present"] =  d["total_present"]+1
# 				exists = True
# 				break
# 		if not exists:
# 				data.append({
# 					"department":r.get("department"),
# 					"total_employee":0,
# 					"total_absent":0,
# 					"late_present":0,
# 					"on_time":0,
# 					"total_present":0

# 				})
		
		
	
# 	return data	

