# # Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# # For license information, please see license.txt

# import frappe

# def execute(filters=None):
# 	columns, data = get_columns(filters), get_data(filters)

# 	return columns, data
# def get_columns(filters):
# 	return[
# 		"Department:Data:120",
# 		# "Biometric ID:Data:80",
# 		"Date:Date:100",
# 			 "Employee:Data:120",
# 			  "Designation:Data:120",
			
# 			"Check In:Data:100",

# 			"Check Out:Data:100",
# 			"Total Hours:Data:100", 
# 			"Late Coming:Data:100",
# 			# "Holidays:Data:50",
# 			# "Halfday:Data:100",
# 			"Early Going:Data:100",
# 			"Over Time:Data:100",
# 			"Status:Data:100"

# 	]
# def get_data(filters):
# 	cond = ""
# 	if filters.get("depart"):
# 		cond = "and emp.department='{0}' ".format(filters.get("depart"))

# 	if filters.get("employee"):
# 		cond = "and emp.employee ='{0}' ".format(filters.get("employee"))
# 	records = frappe.db.sql("""
# 							select
# 							emp.department ,
# 							emp.biometric_id ,
# 							emptab.date,
# 							emp.employee ,
							
# 							emptab.check_in_1,

# 							emptab.check_out_1,
# 							emptab.difference , 
# 							emptab.late_coming_hours,
# 							concat((emptab.sunday)+(emptab.holiday)) as holiday,
# 							emptab.half_day,
# 							IF(emptab.early_going_hours='14:30:00' or emptab.early!=1, "0", emptab.early_going_hours) as early_going_h,
# 							emptab.late_sitting,
# 							emptab.late,
# 							emptab.absent
# 							from  `tabEmployee Attendance` as emp
# 							join `tabEmployee Attendance Table` as emptab on emptab.parent=emp.name
# 							JOIN tabEmployee emply
# 							ON emp.employee = emply.name

# 							where emptab.date = %s {0} and emply.status="Active"
# 							order by emptab.date, emp.department
# 							""".format(cond),(filters.get('to')))

# 	data = []
# 	prev_dep  = None 
# 	total_lates = 0
# 	total_presents = 0
# 	total_absents = 0
# 	for item in records:
# 		row = None
# 		if prev_dep != item[0]:
# 			prev_dep = item[0]
# 			row=[item[0],"","","","","","","","","","","","",]
# 			data.append(row)
# 			row=[""]
# 		else:
# 			row=[""]
# 		# row.append(item[1])
# 		row.append(item[2])
# 		row.append(item[3])
# 		row.append(frappe.db.get_value("Employee",{"name":item[3]},"designation")),
# 		row.append(item[4])
# 		row.append(item[5])
# 		row.append(item[6])
# 		row.append(item[7])
# 		# row.append(item[8])
# 		# row.append(item[9])
# 		row.append(item[10])
# 		row.append(item[11])
# 		status = "<span style='color:blue;'>P</span>"
# 		if item[12] == 1:
# 			status = "<span style='color:green;'>L</span>"
# 			total_lates+=1
# 		elif item[13] == 1:
# 			status = "<span style='color:red;'>A</span>"
# 			total_absents+=1
# 		else:
# 			total_presents+=1
# 		row.append(status)
# 		data.append(row)
# 	data.append([
# 		"","","","","",
# 		"<b>Total Presents</b>",total_presents,
# 		"<b>Total Lates</b>",total_lates,
# 		"<b>Total Absents</b>",total_absents,
# 	])
# 	return data
		