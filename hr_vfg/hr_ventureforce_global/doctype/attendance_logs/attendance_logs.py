# # -*- coding: utf-8 -*-
# # Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# # For license information, please see license.txt

# from __future__ import unicode_literals
# import frappe
# from frappe.model.document import Document
# from frappe.model.document import Document
# from frappe import msgprint, _
# from erpnext.utilities.transaction_base import TransactionBase
# # from erpnext.erpnext.utilities.transaction_base import TransactionBase
# # from frappe.model.naming import make_autoname
# # from frappe.frappe.model.naming import make_autoname
# from frappe.model.naming import make_autoname
# # from frappe.utils import date_diff
# from frappe.utils import date_diff
# from datetime import datetime
# from datetime import timedelta
# import datetime
# import time

# class AttendanceLogs(Document):
# # class AttendanceLogs(TransactionBase):
# 	pass
# 	# def validate(self):
# 	# 	self.get_employee_attendance()

# 	# def get_employee_attendance(self):
# 	# 	mon = ["January", "February", "March", "April", "May", "June", "July", 
# 	# 	"August", "September", "October", "November", "December"]
# 	# 	att_det = str(self.attendance).split()
# 	# 	d = str(att_det[3]).split("-")[1]
# 	# 	month_ = mon[int(d)-1]

# 	# 	start_date = frappe.utils.get_first_day(self.attendance_date)
# 	# 	end_date = frappe.utils.get_last_day(self.attendance_date)
		
		
# 	# 	hr_settings = frappe.get_single('V HR Settings')
# 	# 	if hr_settings.period_from != 1:
# 	# 		if frappe.utils.getdate(self.attendance_date).day < hr_settings.period_from:
# 	# 			tempDate  = frappe.utils.getdate(self.attendance_date)
# 	# 			if (tempDate.month-1) ==0:
# 	# 				start_date = frappe.utils.getdate(str(tempDate.year-1)+"-"+str((tempDate.month-1)+12)+"-"+str(hr_settings.period_from))
# 	# 			else:
# 	# 				start_date = frappe.utils.getdate(str(tempDate.year)+"-"+str((tempDate.month-1))+"-"+str(hr_settings.period_from))
# 	# 			end_date = frappe.utils.getdate(str(tempDate.year)+"-"+str(tempDate.month)+"-"+str(hr_settings.period_to))
# 	# 			month_ = mon[tempDate.month-1]
		
# 	# 		else:
# 	# 			tempDate  = frappe.utils.getdate(self.attendance_date)
# 	# 			start_date = frappe.utils.getdate(str(tempDate.year)+"-"+str(tempDate.month)+"-"+str(hr_settings.period_from))
# 	# 			if tempDate.month == 12:
# 	# 				end_date = frappe.utils.getdate(str(tempDate.year+1)+"-"+str(1)+"-"+str(hr_settings.period_to))
# 	# 			else:
# 	# 				end_date = frappe.utils.getdate(str(tempDate.year)+"-"+str(tempDate.month+1)+"-"+str(hr_settings.period_to))
# 	# 			month_ = mon[tempDate.month]
		
# 	# 	year  = end_date.year
# 	# 	total_days = int(date_diff(end_date, start_date))+1

# 	# 	empl = frappe.db.sql(""" select name, employee_name, branch, department, user_id from `tabEmployee` where biometric_id=%s""", att_det[1])
# 	# 	if empl:
# 	# 		res = frappe.db.sql(""" select name from `tabEmployee Attendance` where employee=%s and month=%s and year=%s""",
# 	# 					(empl[0][0], month_,year))
# 	# 		if res:
# 	# 			if self.type == "Check In":
# 	# 				doc = frappe.get_doc("Employee Attendance", res[0][0])
# 	# 				for x_ in range(len(doc.table1)):
# 	# 					if str(doc.table1[x_].date) == self.attendance_date:
# 	# 						doc.table1[x_].ip = self.ip
# 	# 						doc.table1[x_].check_in_1 = self.attendance_time
# 	# 						#frappe.db.sql("update `tabEmployee Attendance Table` set ip=%s, check_in_1=%s where name=%s",(self.ip,self.attendance_time,doc.table1[x_].name))
# 	# 						break
# 	# 				#frappe.db.commit()
# 	# 				doc.save(ignore_permissions=True)
# 	# 			elif self.type == "Check Out":
# 	# 				doc = frappe.get_doc("Employee Attendance", res[0][0])
# 	# 				for x_ in range(len(doc.table1)):
# 	# 					if str(doc.table1[x_].date) == self.attendance_date:
# 	# 						doc.table1[x_].ip = self.ip
# 	# 						doc.table1[x_].check_out_1 = self.attendance_time
# 	# 						#frappe.db.sql("update `tabEmployee Attendance Table` set ip=%s, check_out_1=%s where name=%s",(self.ip,self.attendance_time,doc.table1[x_].name))
# 	# 						break
# 	# 				#frappe.db.commit()
# 	# 				doc.save(ignore_permissions=True)
# 	# 		else:
# 	# 			today = datetime.date.today()
# 	# 			day_ = datetime.date(today.year, today.month, 1)
# 	# 			single_day = datetime.timedelta(days=1)
# 	# 			m=0
# 	# 			f=0
# 	# 			sat = 0
# 	# 			sun = 0
# 	# 			while day_.month == today.month:
# 	# 				if day_.weekday() == 6:
# 	# 					sun+=1
# 	# 				elif day_.weekday() == 5:
# 	# 					sat+=1
# 	# 				elif day_.weekday() == 4:
# 	# 					f+=1
# 	# 				else:
# 	# 					m+=1
# 	# 				day_ += single_day

# 	# 			doc = frappe.new_doc("Employee Attendance")
# 	# 			doc.employee = empl[0][0]
# 	# 			doc.employee_name = empl[0][1]
# 	# 			doc.biometric_id = att_det[1]
# 	# 			doc.month = month_
# 	# 			doc.year = year
# 	# 			da = start_date
# 	# 			doc.unit = empl[0][2]
# 	# 			doc.department = empl[0][3]
# 	# 			doc.email_id = empl[0][4]
# 	# 			#doc.total_working_hours = (int(empl[0][4])*m)+(int(empl[0][5])*f)+(int(empl[0][6])*sat)+(int(empl[0][7])*sun)
# 	# 			for x in range(total_days):
# 	# 				pi = doc.append('table1', {"check_in_1":None,"check_out_1":None})
# 	# 				pi.date = da
# 	# 				if str(da) == str(self.attendance_date):
# 	# 					if self.type == "Check In":
# 	# 						pi.check_in_1 = att_det[4]
# 	# 					if self.type == "Check Out":
# 	# 						pi.check_out_1 = att_det[4]
# 	# 				else:
# 	# 					pi.check_in_1 = hr_settings.auto_fetch_check_in
# 	# 					pi.check_out_1 = hr_settings.auto_fetch_check_out
# 	# 				da = da + timedelta(days=1)
# 	# 			doc.save(ignore_permissions=True)