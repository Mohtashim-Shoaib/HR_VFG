# from __future__ import unicode_literals
import frappe
from frappe import utils
# from frappe import throw, _

# import sys
# import time
# from zk import ZK, const
# from datetime import datetime, timedelta
# from frappe.utils import date_diff, add_months, get_datetime, today, getdate, add_days, flt, get_last_day
# import calendar
# from frappe.utils.background_jobs import enqueue
# from requests import request
# import json
# from datetime import datetime
# from datetime import timedelta


# @frappe.whitelist()
# def get_attendance_long(**args):
# 	if not args:
# 		args = frappe.local.form_dict
# 	"Enqueue longjob for taking backup to dropbox"
# 	#enqueue("erpnext.hr.doctype.attendance.att_week.get_attendance_in_test", queue='long', timeout=1500)
# 	enqueue("erpnext.hr.doctype.attendance.att_week.get_attendance_in_test2", queue='long', timeout=5000,args=args)
# 	# enqueue("erpnext.hr.doctype.attendance.att_week.get_attendance_in_test3", queue='long', timeout=5000,args=args)
# 	# enqueue("erpnext.hr.doctype.attendance.att_week.get_attendance_in_test4", queue='long', timeout=5000,args=args)

# 	#enqueue("erpnext.hr.doctype.attendance.att_week.get_attendance_out", queue='long', timeout=1500)
# 	frappe.msgprint(_("Queued for biometric attendance. It may take a few minutes to an hour."))
# @frappe.whitelist()
# def settle_night_s():
# 	"Enqueue longjob for taking backup to dropbox"
# 	enqueue("erpnext.hr.doctype.attendance.att_week.settle_night_shift", queue='long', timeout=3000)
# 	frappe.msgprint(_("Queued for night shift settlment."))
# def get_attendance_in():
# 	conn = None
# 	emp_list = []
# 	zk = ZK('115.167.64.233', port=int(4370), timeout=1500, password=0, force_udp=False, ommit_ping=False)
# 	try:
# 		conn = zk.connect()
# 		if conn:
# 			users = conn.get_users()
# 			if users:
# 				for u in users:
# 					print(u)

# 			attendance = conn.get_attendance()
# 			if attendance:
# 				print(attendance)
# 				atten_date_ = str(datetime.strptime(str(utils.today()), '%Y-%m-%d') - timedelta(days=1)).split()[0]
# 				for attend1 in attendance:
# 					d_a = str(utils.today()) +" 8:30:0"
# 					d_b = str(utils.today()) +" 1:0:0"
# 					d_s = str(utils.today()) +" 23:59:00"
# 					d_c = str(attend1).split()[3]+" "+str(attend1).split()[4]

# 					date_a = datetime.strptime(d_a, '%Y-%m-%d %H:%M:%S') - timedelta(days=8)
# 					date_b = datetime.strptime(d_s, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)
# 					date_c = datetime.strptime(d_c, '%Y-%m-%d %H:%M:%S')

# 					if date_c >= date_a and date_c <= date_b:
# 						res = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
# 							biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check In'""", 
# 							(str(attend1).split()[1], str(attend1).split()[3], str(attend1).split()[4]))
# 						if res:
# 							#frappe.db.set_value("Attendance Logs", res[0][0], "biometric_id", res[0][1])
# 							atl = frappe.get_doc("Attendance Logs",res[0][0])
# 							atl.save()
# 						else:
# 							doc1 = frappe.new_doc("Attendance Logs")
# 							doc1.attendance = str(attend1)
# 							doc1.biometric_id= str(attend1).split()[1]
# 							doc1.attendance_date= str(attend1).split()[3]
# 							doc1.attendance_time= str(attend1).split()[4]
# 							doc1.type = "Check In"
# 							doc1.save()
# 	except Exception as e:
# 		print ("Process terminate : {}".format(e))
# 	finally:
# 		if conn:
# 			conn.disconnect()

# def get_attendance_out():
# 	conn = None
# 	emp_list = []
# 	zk = ZK('115.167.64.233', port=int(4370), timeout=1500, password=0, force_udp=False, ommit_ping=False)
# 	try:
# 		conn = zk.connect()
# 		if conn:
# 			users = conn.get_users()
# 			if users:
# 				for u in users:
# 					print(u)
# 			attendance = conn.get_attendance()
# 			if attendance:
# 				print(attendance)
# 				atten_date_ = str(datetime.strptime(str(utils.today()), '%Y-%m-%d') - timedelta(days=1)).split()[0]
# 				for attend1 in attendance:
# 					d_a = str(utils.today()) +" 8:30:0"
# 					d_b = str(utils.today()) +" 1:0:0"
# 					d_s = str(utils.today()) +" 23:59:00"
# 					d_c = str(attend1).split()[3]+" "+str(attend1).split()[4]

# 					date_a = datetime.strptime(d_a, '%Y-%m-%d %H:%M:%S') - timedelta(days=8)
# 					date_b = datetime.strptime(d_s, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)
# 					date_c = datetime.strptime(d_c, '%Y-%m-%d %H:%M:%S')

# 					if date_c >= date_a and date_c <= date_b:
# 						res = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
# 							biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check Out'""", 
# 							(str(attend1).split()[1], str(attend1).split()[3], str(attend1).split()[4]))
# 						if res:
# 							#frappe.db.set_value("Attendance Logs", res[0][0], "biometric_id", res[0][1])
# 							atl = frappe.get_doc("Attendance Logs",res[0][0])
# 							atl.save()
# 						else:
# 							doc1 = frappe.new_doc("Attendance Logs")
# 							doc1.attendance = str(attend1)
# 							doc1.biometric_id= str(attend1).split()[1]
# 							doc1.attendance_date= str(attend1).split()[3]
# 							doc1.attendance_time= str(attend1).split()[4]
# 							doc1.type = "Check Out"
# 							doc1.save()
# 	except Exception as e:
# 		print ("Process terminate : {}".format(e))
# 	finally:
# 		if conn:
# 			conn.disconnect()

# def get_attendance_in_test():
# 	conn = None
# 	emp_list = [] #110.93.236.48
# 	zk = ZK('115.167.64.233', port=int(4370), timeout=1500, password=0, force_udp=False, ommit_ping=False)
# 	try:
# 		conn = zk.connect()
# 		if conn:
# 			users = conn.get_users()
# 			if users:
# 				for u in users:
# 					#print(u)
# 					pass

# 			attendance = conn.get_attendance()
# 			print("getting attendance data")
# 			print(attendance)
# 			if attendance:
# 				print(attendance)
				
# 				attendance_dict={}
# 				for attend1 in attendance[-13:]:
# 					if attendance_dict.get(str(attend1).split()[1]):
# 						if attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3]):
# 							attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3])["check out"]=str(attend1).split()[4]
# 							attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3])["checkout string"]=str(attend1)
# 						else:
# 							attendance_dict.get(str(attend1).split()[1])[str(attend1).split()[3]]={
# 								"check in": str(attend1).split()[4],
# 								"checkin string":str(attend1)
# 							}
# 					else:
# 						attendance_dict[str(attend1).split()[1]]={
# 							str(attend1).split()[3] :{
# 								"check in": str(attend1).split()[4],
# 								"checkin string":str(attend1)
# 							}
# 						}
					

# 				import json
# 				#print(attendance_dict)
# 				for users in attendance_dict:
# 					print(users)
# 					for dates in attendance_dict[users]:
# 						try:
# 							date = dates
# 							check_in = attendance_dict[users][dates].get("check in")
# 							check_in_string = attendance_dict[users][dates].get("checkin string")
# 							check_out = attendance_dict[users][dates].get("check out")
# 							check_out_string = attendance_dict[users][dates].get("checkout string")
# 							if check_in:
# 									d_a = str(utils.today()) +" 8:30:0"
# 									d_b = str(utils.today()) +" 1:0:0"
# 									d_s = str(utils.today()) +" 23:59:00"
# 									d_c = str(date+" "+check_in)

# 									date_a = datetime.strptime(d_a, '%Y-%m-%d %H:%M:%S') - timedelta(days=25)
# 									date_b = datetime.strptime(d_s, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)
# 									date_c = datetime.strptime(d_c, '%Y-%m-%d %H:%M:%S')
# 									if date_c >= date_a and date_c <= date_b:
# 										res = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
# 										biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check In'""", 
# 										(users, date, check_in))
# 										if res:
# 											# frappe.db.set_value("Attendance Logs", res[0][0], "biometric_id", res[0][1])
# 											# frappe.db.set_value("Attendance Logs", res[0][0], "ip", '115.167.64.233')
# 											atl = frappe.get_doc("Attendance Logs",res[0][0])
# 											atl.save()
# 										else:
# 											doc1 = frappe.new_doc("Attendance Logs")
# 											doc1.attendance = check_in_string
# 											doc1.biometric_id= users
# 											doc1.attendance_date= str(date)
# 											doc1.attendance_time= str(check_in)
# 											doc1.type = "Check In"
# 											doc1.ip = '115.167.64.233'
# 											doc1.save()
# 							if check_out:
# 									print(check_out)
# 									d_a = str(utils.today()) +" 8:30:0"
# 									d_b = str(utils.today()) +" 1:0:0"
# 									d_s = str(utils.today()) +" 23:59:00"
# 									d_c = str(date+" "+check_out)

# 									date_a = datetime.strptime(d_a, '%Y-%m-%d %H:%M:%S') - timedelta(days=25)
# 									date_b = datetime.strptime(d_s, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)
# 									date_c = datetime.strptime(d_c, '%Y-%m-%d %H:%M:%S')
# 									if date_c >= date_a and date_c <= date_b:
# 										res = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
# 										biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check In'""", 
# 										(users, date, check_out))
# 										if res:
# 											# frappe.db.set_value("Attendance Logs", res[0][0], "biometric_id", res[0][1])
# 											# frappe.db.set_value("Attendance Logs", res[0][0], "ip", '101.53.249.253')
# 											atl = frappe.get_doc("Attendance Logs",res[0][0])
# 											atl.save()
# 										else:
# 											doc2 = frappe.new_doc("Attendance Logs")
# 											doc2.attendance = check_out_string
# 											doc2.biometric_id= users
# 											doc2.attendance_date= str(date)
# 											doc2.attendance_time= str(check_out)
# 											doc2.type = "Check Out"
# 											doc2.ip = '115.167.64.233'
# 											doc2.save()
# 						except:
# 							frappe.log_error(frappe.get_traceback(),"Attendance hook test")
# 				f = open("/home/frappe/frappe-bench/attendance.json", "a")
# 				f.write(json.dumps(str(attendance)))
# 				f.close()
# 				print(len(attendance))
# 	except Exception as e:
# 		print ("Process terminate : {}"+frappe.get_traceback())
# 	finally:
# 		if conn:
# 			conn.disconnect()


# def get_attendance_in_test2(args):
# 	conn = None
# 	emp_list = [] #110.93.236.48
# 	zk = ZK('115.167.64.233', port=int(4370), timeout=1500, password=0, force_udp=False, ommit_ping=False)
# 	try:
# 		conn = zk.connect()
# 		if conn:
# 			users = conn.get_users()
# 			if users:
# 				for u in users:
# 					#print(u)
# 					pass

# 			attendance = conn.get_attendance()
# 			print("getting attendance data")
# 			#print(attendance)
# 			if attendance:
# 				#print(attendance)
				
# 				attendance_dict={}
# 				condition1 =""
# 				condition2=""
# 				biometric_list=[]
# 				b_filters = {}
# 				if args.get("employee"):
# 					condition1=" and parent in (select name from `tabEmployee Attendance` where employee='{0}')".format(args.get("employee"))
# 					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where name='{0}')".format(args.get("employee"))
# 					b_filters["name"]=args.get("employee")
# 				if args.get("department"):
# 					condition1=" and parent in (select name from `tabEmployee Attendance` where department='{0}')".format(args.get("department"))
# 					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where department='{0}')".format(args.get("department"))
# 					b_filters["department"]=args.get("department")
# 				if args.get("employee") and args.get("department"):
# 					condition1=" and parent in (select name from `tabEmployee Attendance` where employee='{0}' and department='{1}')".format(args.get("employee"),args.get("department"))
# 					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where name='{0}' and department='{1}')".format(args.get("employee"),args.get("department"))

# 				B_r = frappe.db.get_all("Employee",filters=b_filters,fields=["biometric_id"])
# 				for bid in B_r:
# 					biometric_list.append(bid.biometric_id)
# 				frappe.db.sql(""" delete from `tabAttendance Logs` where attendance_date >= %s and attendance_date <= %s and ip="115.167.64.233:4370"{0} """.format(condition2), (args.get("from_date"),args.get("to_date")))
# 				frappe.db.sql(""" update `tabEmployee Attendance Table` set check_in_1=NULL, check_out_1=NULL, late_sitting=NULL, night_switch=0 where date >= %s and date <= %s and ip="115.167.64.233:4370"{0} """.format(condition1), (args.get("from_date"),args.get("to_date")))
# 				frappe.db.commit()
# 				for attend1 in attendance:
# 					if getdate(str(attend1).split()[3]) < getdate(args.get("from_date")) or getdate(str(attend1).split()[3]) > getdate(args.get("to_date")):
# 						continue
# 					if len(biometric_list) > 0:
# 						if str(attend1).split()[1] not in biometric_list:
# 							continue
# 					if attendance_dict.get(str(attend1).split()[1]):
# 						if attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3]):
# 							attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3])["check out"]=str(attend1).split()[4]
# 							attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3])["checkout string"]=str(attend1)
# 						else:
# 							attendance_dict.get(str(attend1).split()[1])[str(attend1).split()[3]]={
# 								"check in": str(attend1).split()[4],
# 								"checkin string":str(attend1)
# 							}
# 					else:
# 						attendance_dict[str(attend1).split()[1]]={
# 							str(attend1).split()[3] :{
# 								"check in": str(attend1).split()[4],
# 								"checkin string":str(attend1)
# 							}
# 						}
					
					

# 				import json
# 				#print(attendance_dict)
# 				for users in attendance_dict:
# 					#print(users)
# 					for dates in attendance_dict[users]:
# 						try:
# 							date = dates
# 							check_in = attendance_dict[users][dates].get("check in")
# 							check_in_string = attendance_dict[users][dates].get("checkin string")
# 							check_out = attendance_dict[users][dates].get("check out")
# 							check_out_string = attendance_dict[users][dates].get("checkout string")
# 							# print(check_in) 
# 							# print("_____________________________________________")
# 							# print(check_out)
# 							# print("_____________________________________________")
# 							temp_chk_in = None
# 							if check_in:
# 									d_a = str(utils.today()) +" 8:30:0"
# 									d_b = str(utils.today()) +" 1:0:0"
# 									d_s = str(utils.today()) +" 23:59:00"
# 									d_c = str(date+" "+check_in)
# 									temp_chk_in = check_in

									
# 									date_a = datetime.strptime(d_a, '%Y-%m-%d %H:%M:%S') - timedelta(days=25)
# 									date_b = datetime.strptime(d_s, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)
# 									date_c = datetime.strptime(d_c, '%Y-%m-%d %H:%M:%S')
# 									#print("date a")
# 									#print(date_a)
# 									# print("date b")
# 									# print(date_b)
# 									# print("date c")
# 									# print(date_c)
# 									#if date_c >= date_a and date_c <= date_b:
# 									res = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
# 									biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check In'""", 
# 									(users, str(date), check_in))
# 									if res:
# 										# frappe.db.set_value("Attendance Logs", res[0][0], "biometric_id", res[0][1])
# 										# frappe.db.set_value("Attendance Logs", res[0][0], "ip", '202.143.127.8')
# 										atl = frappe.get_doc("Attendance Logs",res[0][0])
# 										atl.save()
# 									else:
# 										print("adding check in")
# 										doc1 = frappe.new_doc("Attendance Logs")
# 										doc1.attendance = check_in_string
# 										doc1.biometric_id= users
# 										doc1.attendance_date= str(date)
# 										doc1.attendance_time= str(check_in)
# 										doc1.type = "Check In"
# 										doc1.ip = '115.167.64.233:4370'
# 										doc1.save()
# 							if check_out:
# 									# print("In check out")
# 									# print(check_in)
# 									if check_in:
# 										x = datetime.strptime(
#                         					str(temp_chk_in), '%H:%M:%S').time()
# 										y = datetime.strptime(
#                         					str(check_out), '%H:%M:%S').time()
# 										hi,mi,si = str(x).split(':')
# 										ho,mo,so = str(y).split(':')
# 										diff_time = timedelta(hours=0, minutes=30, seconds=0)
										
# 										if (timedelta(hours=float(ho), minutes=float(mo), seconds=float(so))-timedelta(hours=float(hi), minutes=float(mi), seconds=float(si))) < diff_time:
# 											continue

									
# 									d_a = str(utils.today()) +" 8:30:0"
# 									d_b = str(utils.today()) +" 1:0:0"
# 									d_s = str(utils.today()) +" 23:59:00"
# 									d_c = str(date+" "+check_out)

# 									print("date a")
# 									print(date_a)
# 									print("date b")
# 									print(date_b)
# 									print("date c")
# 									print(date_c)
# 									date_a = datetime.strptime(d_a, '%Y-%m-%d %H:%M:%S') - timedelta(days=25)
# 									date_b = datetime.strptime(d_s, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)
# 									date_c = datetime.strptime(d_c, '%Y-%m-%d %H:%M:%S')
# 									#if date_c >= date_a and date_c <= date_b:
# 									res = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
# 									biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check Out'""", 
# 									(users, str(date), check_out))
# 									if res:
# 										# frappe.db.set_value("Attendance Logs", res[0][0], "biometric_id", res[0][1])
# 										# frappe.db.set_value("Attendance Logs", res[0][0], "ip", '115.167.64.233')
# 										atl = frappe.get_doc("Attendance Logs",res[0][0])
# 										atl.save()
# 									else:
# 										print("adding check out")
# 										doc2 = frappe.new_doc("Attendance Logs")
# 										doc2.attendance = check_out_string
# 										doc2.biometric_id= users
# 										doc2.attendance_date= str(date)
# 										doc2.attendance_time= str(check_out)
# 										doc2.type = "Check Out"
# 										doc2.ip = '115.167.64.233:4370'
# 										doc2.save()
# 						except:
# 							frappe.log_error(frappe.get_traceback(),"Attendance hook test")
# 				f = open("/home/frappe/frappe-bench/attendance.json", "a")
# 				f.write(json.dumps(str(attendance)))
# 				f.close()
# 				#settle_night_s()
# 				print(len(attendance))
				
# 	except Exception as e:
# 		print ("Process terminate : {}"+frappe.get_traceback())
# 	finally:
# 		if conn:
# 			conn.disconnect()



# def settle_night_shift():
# 	EL  = frappe.get_all("Employee Attendance",filters={},fields=["name"])
# 	for data in EL:
# 		try:
# 			doc = frappe.get_doc("Employee Attendance",data.name)
# 			#frappe.log_error(len(doc.table1),"Night shift doc")
# 			for item in range(len(doc.table1)):
# 					try:
# 						if doc.table1[item].night_switch == 1:
# 							continue
# 						shift_req = frappe.get_all("Shift Request", filters={'employee': doc.employee,
# 																		'from_date': ["<=", doc.table1[item].date], 'to_date': [">=", doc.table1[item].date]}, fields=["*"])
# 						shift = None
# 						if len(shift_req) > 0:
# 							shift = shift_req[0].shift_type
# 						else:
# 							shift_ass = frappe.get_all("Shift Assignment", filters={'employee': doc.employee,
# 																					'date': ["<=", doc.table1[item].date]}, fields=["*"])
# 							if len(shift_ass) > 0:
# 								shift = shift_ass[0].shift_type
# 						shift_doc = frappe.get_doc("Shift Type", shift)
						
# 						if shift_doc.shift_type == "Night" and item == 1:
# 							if doc.table1[item].check_in_1 and  doc.table1[item].check_out_1:
# 								y = datetime.strptime(
#                         					str(doc.table1[item].check_in_1), '%H:%M:%S').time()
	
# 								ho,mo,so = str(y).split(':')
# 								if timedelta(hours=float(ho), minutes=float(mo), seconds=float(so)) < timedelta(hours=18, minutes=0, seconds=0):
# 									doc.table1[item -1].check_out_1 =doc.table1[item].check_in_1
# 								doc.table1[item-1].night_switch = 1
# 							elif doc.table1[item].check_in_1 and not doc.table1[item].check_out_1:
# 								y = datetime.strptime(
#                         					str(doc.table1[item].check_in_1), '%H:%M:%S').time()
	
# 								ho,mo,so = str(y).split(':')
# 								if timedelta(hours=float(ho), minutes=float(mo), seconds=float(so)) > timedelta(hours=18, minutes=0, seconds=0):
# 									doc.table1[item].check_out_1 =doc.table1[item].check_in_1
# 								else:
# 									doc.table1[item -1].check_out_1 =doc.table1[item].check_in_1
# 								doc.table1[item-1].night_switch = 1
							
# 						if shift_doc.shift_type == "Night" and item > 1:
# 							doc.table1[item -1].check_in_1 =doc.table1[item-1].check_out_1
# 							doc.table1[item -1].check_out_1 =None
# 							if doc.table1[item].check_in_1 and  doc.table1[item].check_out_1:
# 								y = datetime.strptime(
#                         					str(doc.table1[item].check_in_1), '%H:%M:%S').time()
	
# 								ho,mo,so = str(y).split(':')
# 								if timedelta(hours=float(ho), minutes=float(mo), seconds=float(so)) < timedelta(hours=18, minutes=0, seconds=0):
# 									doc.table1[item -1].check_out_1 =doc.table1[item].check_in_1
# 								doc.table1[item-1].night_switch = 1
								
# 							elif doc.table1[item].check_in_1 and not doc.table1[item].check_out_1:
# 									y = datetime.strptime(
# 												str(doc.table1[item].check_in_1), '%H:%M:%S').time()
		
# 									ho,mo,so = str(y).split(':')
# 									if timedelta(hours=float(ho), minutes=float(mo), seconds=float(so)) > timedelta(hours=18, minutes=0, seconds=0):
# 										doc.table1[item].check_out_1 =doc.table1[item].check_in_1
# 									else:
# 										doc.table1[item -1].check_out_1 =doc.table1[item].check_in_1
# 									doc.table1[item-1].night_switch = 1
# 						if not doc.table1[item -1].check_in_1 and not doc.table1[item -1].check_out_1:
# 							doc.table1[item-1].night_switch = 0
# 					except:
# 						frappe.log_error(frappe.get_traceback(),"Night shift settle")
# 			doc.save()
# 		except:
# 			frappe.log_error(frappe.get_traceback(),"Night shift")

# def get_attendance_in_test3(args):
# 	conn = None
# 	emp_list = [] #110.93.236.48
# 	zk = ZK('115.167.64.233', port=int(4370), timeout=1500, password=0, force_udp=False, ommit_ping=False)
# 	try:
# 		conn = zk.connect()
# 		if conn:
# 			users = conn.get_users()
# 			if users:
# 				for u in users:
# 					#print(u)
# 					pass

# 			attendance = conn.get_attendance()
# 			print("getting attendance data")
# 			#print(attendance)
# 			if attendance:
# 				#print(attendance)
				
# 				attendance_dict={}
# 				condition1 =""
# 				condition2=""
# 				biometric_list=[]
# 				b_filters = {}
# 				if args.get("employee"):
# 					condition1=" and parent in (select name from `tabEmployee Attendance` where employee='{0}')".format(args.get("employee"))
# 					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where name='{0}')".format(args.get("employee"))
# 					b_filters["name"]=args.get("employee")
# 				if args.get("department"):
# 					condition1=" and parent in (select name from `tabEmployee Attendance` where department='{0}')".format(args.get("department"))
# 					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where department='{0}')".format(args.get("department"))
# 					b_filters["department"]=args.get("department")
# 				if args.get("employee") and args.get("department"):
# 					condition1=" and parent in (select name from `tabEmployee Attendance` where employee='{0}' and department='{1}')".format(args.get("employee"),args.get("department"))
# 					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where name='{0}' and department='{1}')".format(args.get("employee"),args.get("department"))

# 				B_r = frappe.db.get_all("Employee",filters=b_filters,fields=["biometric_id"])
# 				for bid in B_r:
# 					biometric_list.append(bid.biometric_id)
# 				frappe.db.sql(""" delete from `tabAttendance Logs` where attendance_date >= %s and attendance_date <= %s and ip="115.167.64.233:4370"{0} """.format(condition2), (args.get("from_date"),args.get("to_date")))
# 				frappe.db.sql(""" update `tabEmployee Attendance Table` set check_in_1=NULL, check_out_1=NULL, late_sitting=NULL, night_switch=0 where date >= %s and date <= %s and ip="115.167.64.233:4370"{0} """.format(condition1), (args.get("from_date"),args.get("to_date")))
# 				frappe.db.commit()
# 				for attend1 in attendance:
# 					if getdate(str(attend1).split()[3]) < getdate(args.get("from_date")) or getdate(str(attend1).split()[3]) > getdate(args.get("to_date")):
# 						continue
# 					if len(biometric_list) > 0:
# 						if str(attend1).split()[1] not in biometric_list:
# 							continue
# 					if attendance_dict.get(str(attend1).split()[1]):
# 						if attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3]):
# 							attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3])["check out"]=str(attend1).split()[4]
# 							attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3])["checkout string"]=str(attend1)
# 						else:
# 							attendance_dict.get(str(attend1).split()[1])[str(attend1).split()[3]]={
# 								"check in": str(attend1).split()[4],
# 								"checkin string":str(attend1)
# 							}
# 					else:
# 						attendance_dict[str(attend1).split()[1]]={
# 							str(attend1).split()[3] :{
# 								"check in": str(attend1).split()[4],
# 								"checkin string":str(attend1)
# 							}
# 						}
					
					

# 				import json
# 				#print(attendance_dict)
# 				for users in attendance_dict:
# 					print(users)
# 					for dates in attendance_dict[users]:
# 						try:
# 							date = dates
# 							check_in = attendance_dict[users][dates].get("check in")
# 							check_in_string = attendance_dict[users][dates].get("checkin string")
# 							check_out = attendance_dict[users][dates].get("check out")
# 							check_out_string = attendance_dict[users][dates].get("checkout string")
# 							# print(check_in) 
# 							# print("_____________________________________________")
# 							# print(check_out)
# 							# print("_____________________________________________")
# 							temp_chk_in = None
# 							if check_in:
# 									d_a = str(utils.today()) +" 8:30:0"
# 									d_b = str(utils.today()) +" 1:0:0"
# 									d_s = str(utils.today()) +" 23:59:00"
# 									d_c = str(date+" "+check_in)
# 									temp_chk_in = check_in

									
# 									date_a = datetime.strptime(d_a, '%Y-%m-%d %H:%M:%S') - timedelta(days=25)
# 									date_b = datetime.strptime(d_s, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)
# 									date_c = datetime.strptime(d_c, '%Y-%m-%d %H:%M:%S')
# 									#print("date a")
# 									#print(date_a)
# 									# print("date b")
# 									# print(date_b)
# 									# print("date c")
# 									# print(date_c)
# 									#if date_c >= date_a and date_c <= date_b:
# 									res = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
# 									biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check In'""", 
# 									(users, str(date), check_in))
# 									if res:
# 										# frappe.db.set_value("Attendance Logs", res[0][0], "biometric_id", res[0][1])
# 										# frappe.db.set_value("Attendance Logs", res[0][0], "ip", '202.143.127.8')
# 										atl = frappe.get_doc("Attendance Logs",res[0][0])
# 										atl.save()
# 									else:
# 										print("adding check in")
# 										doc1 = frappe.new_doc("Attendance Logs")
# 										doc1.attendance = check_in_string
# 										doc1.biometric_id= users
# 										doc1.attendance_date= str(date)
# 										doc1.attendance_time= str(check_in)
# 										doc1.type = "Check In"
# 										doc1.ip = '115.167.64.233:4370'
# 										doc1.save()
# 							if check_out:
# 									# print("In check out")
# 									# print(check_in)
# 									if check_in:
# 										x = datetime.strptime(
#                         					str(temp_chk_in), '%H:%M:%S').time()
# 										y = datetime.strptime(
#                         					str(check_out), '%H:%M:%S').time()
# 										hi,mi,si = str(x).split(':')
# 										ho,mo,so = str(y).split(':')
# 										diff_time = timedelta(hours=0, minutes=30, seconds=0)
										
# 										if (timedelta(hours=float(ho), minutes=float(mo), seconds=float(so))-timedelta(hours=float(hi), minutes=float(mi), seconds=float(si))) < diff_time:
# 											continue

									
# 									d_a = str(utils.today()) +" 8:30:0"
# 									d_b = str(utils.today()) +" 1:0:0"
# 									d_s = str(utils.today()) +" 23:59:00"
# 									d_c = str(date+" "+check_out)

# 									print("date a")
# 									print(date_a)
# 									print("date b")
# 									print(date_b)
# 									print("date c")
# 									print(date_c)
# 									date_a = datetime.strptime(d_a, '%Y-%m-%d %H:%M:%S') - timedelta(days=25)
# 									date_b = datetime.strptime(d_s, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)
# 									date_c = datetime.strptime(d_c, '%Y-%m-%d %H:%M:%S')
# 									#if date_c >= date_a and date_c <= date_b:
# 									res = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
# 									biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check Out'""", 
# 									(users, str(date), check_out))
# 									if res:
# 										# frappe.db.set_value("Attendance Logs", res[0][0], "biometric_id", res[0][1])
# 										# frappe.db.set_value("Attendance Logs", res[0][0], "ip", '202.143.127.8')
# 										atl = frappe.get_doc("Attendance Logs",res[0][0])
# 										atl.save()
# 									else:
# 										print("adding check out")
# 										doc2 = frappe.new_doc("Attendance Logs")
# 										doc2.attendance = check_out_string
# 										doc2.biometric_id= users
# 										doc2.attendance_date= str(date)
# 										doc2.attendance_time= str(check_out)
# 										doc2.type = "Check Out"
# 										doc2.ip = '115.167.64.233:4370'
# 										doc2.save()
# 						except:
# 							frappe.log_error(frappe.get_traceback(),"Attendance hook test")
# 				f = open("/home/frappe/frappe-bench/attendance_from_new_mach.json", "a")
# 				f.write(json.dumps(str(attendance)))
# 				f.close()
# 				settle_night_s()
# 				print(len(attendance))
				
# 	except Exception as e:
# 		print ("Process terminate : {}"+frappe.get_traceback())
# 	finally:
# 		if conn:
# 			conn.disconnect()




# def get_attendance_in_test4(args):
# 	conn = None
# 	emp_list = [] #110.93.236.48
# 	zk = ZK('115.167.64.233', port=int(4370), timeout=1500, password=0, force_udp=False, ommit_ping=False)
# 	try:
# 		conn = zk.connect()
# 		if conn:
# 			users = conn.get_users()
# 			if users:
# 				for u in users:
# 					#print(u)
# 					pass

# 			attendance = conn.get_attendance()
# 			print("getting attendance data")
# 			#print(attendance)
# 			if attendance:
# 				#print(attendance)
				
# 				attendance_dict={}
# 				condition1 =""
# 				condition2=""
# 				biometric_list=[]
# 				b_filters = {}
# 				if args.get("employee"):
# 					condition1=" and parent in (select name from `tabEmployee Attendance` where employee='{0}')".format(args.get("employee"))
# 					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where name='{0}')".format(args.get("employee"))
# 					b_filters["name"]=args.get("employee")
# 				if args.get("department"):
# 					condition1=" and parent in (select name from `tabEmployee Attendance` where department='{0}')".format(args.get("department"))
# 					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where department='{0}')".format(args.get("department"))
# 					b_filters["department"]=args.get("department")
# 				if args.get("employee") and args.get("department"):
# 					condition1=" and parent in (select name from `tabEmployee Attendance` where employee='{0}' and department='{1}')".format(args.get("employee"),args.get("department"))
# 					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where name='{0}' and department='{1}')".format(args.get("employee"),args.get("department"))

# 				B_r = frappe.db.get_all("Employee",filters=b_filters,fields=["biometric_id"])
# 				for bid in B_r:
# 					biometric_list.append(bid.biometric_id)
# 				frappe.db.sql(""" delete from `tabAttendance Logs` where attendance_date >= %s and attendance_date <= %s and ip="103.53.44.158:4380"{0} """.format(condition2), (args.get("from_date"),args.get("to_date")))
# 				frappe.db.sql(""" update `tabEmployee Attendance Table` set check_in_1=NULL, check_out_1=NULL, late_sitting=NULL, night_switch=0 where date >= %s and date <= %s and ip="103.53.44.158:4380"{0} """.format(condition1), (args.get("from_date"),args.get("to_date")))
# 				frappe.db.commit()
# 				for attend1 in attendance:
# 					if getdate(str(attend1).split()[3]) < getdate(args.get("from_date")) or getdate(str(attend1).split()[3]) > getdate(args.get("to_date")):
# 						continue
# 					if len(biometric_list) > 0:
# 						if str(attend1).split()[1] not in biometric_list:
# 							continue
# 					if attendance_dict.get(str(attend1).split()[1]):
# 						if attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3]):
# 							attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3])["check out"]=str(attend1).split()[4]
# 							attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3])["checkout string"]=str(attend1)
# 						else:
# 							attendance_dict.get(str(attend1).split()[1])[str(attend1).split()[3]]={
# 								"check in": str(attend1).split()[4],
# 								"checkin string":str(attend1)
# 							}
# 					else:
# 						attendance_dict[str(attend1).split()[1]]={
# 							str(attend1).split()[3] :{
# 								"check in": str(attend1).split()[4],
# 								"checkin string":str(attend1)
# 							}
# 						}
					
					

# 				import json
# 				#print(attendance_dict)
# 				for users in attendance_dict:
# 					#print(users)
# 					for dates in attendance_dict[users]:
# 						try:
# 							date = dates
# 							check_in = attendance_dict[users][dates].get("check in")
# 							check_in_string = attendance_dict[users][dates].get("checkin string")
# 							check_out = attendance_dict[users][dates].get("check out")
# 							check_out_string = attendance_dict[users][dates].get("checkout string")
# 							# print(check_in) 
# 							# print("_____________________________________________")
# 							# print(check_out)
# 							# print("_____________________________________________")
# 							temp_chk_in = None
# 							if check_in:
# 									d_a = str(utils.today()) +" 8:30:0"
# 									d_b = str(utils.today()) +" 1:0:0"
# 									d_s = str(utils.today()) +" 23:59:00"
# 									d_c = str(date+" "+check_in)
# 									temp_chk_in = check_in

									
# 									date_a = datetime.strptime(d_a, '%Y-%m-%d %H:%M:%S') - timedelta(days=25)
# 									date_b = datetime.strptime(d_s, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)
# 									date_c = datetime.strptime(d_c, '%Y-%m-%d %H:%M:%S')
# 									#print("date a")
# 									#print(date_a)
# 									# print("date b")
# 									# print(date_b)
# 									# print("date c")
# 									# print(date_c)
# 									#if date_c >= date_a and date_c <= date_b:
# 									res = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
# 									biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check In'""", 
# 									(users, str(date), check_in))
# 									if res:
# 										# frappe.db.set_value("Attendance Logs", res[0][0], "biometric_id", res[0][1])
# 										# frappe.db.set_value("Attendance Logs", res[0][0], "ip", '202.143.127.8')
# 										atl = frappe.get_doc("Attendance Logs",res[0][0])
# 										atl.save()
# 									else:
# 										print("adding check in")
# 										doc1 = frappe.new_doc("Attendance Logs")
# 										doc1.attendance = check_in_string
# 										doc1.biometric_id= users
# 										doc1.attendance_date= str(date)
# 										doc1.attendance_time= str(check_in)
# 										doc1.type = "Check In"
# 										doc1.ip = '115.167.64.233:4370'
# 										doc1.save()
# 							if check_out:
# 									# print("In check out")
# 									# print(check_in)
# 									if check_in:
# 										x = datetime.strptime(
#                         					str(temp_chk_in), '%H:%M:%S').time()
# 										y = datetime.strptime(
#                         					str(check_out), '%H:%M:%S').time()
# 										hi,mi,si = str(x).split(':')
# 										ho,mo,so = str(y).split(':')
# 										diff_time = timedelta(hours=0, minutes=30, seconds=0)
										
# 										if (timedelta(hours=float(ho), minutes=float(mo), seconds=float(so))-timedelta(hours=float(hi), minutes=float(mi), seconds=float(si))) < diff_time:
# 											continue

									
# 									d_a = str(utils.today()) +" 8:30:0"
# 									d_b = str(utils.today()) +" 1:0:0"
# 									d_s = str(utils.today()) +" 23:59:00"
# 									d_c = str(date+" "+check_out)

# 									print("date a")
# 									print(date_a)
# 									print("date b")
# 									print(date_b)
# 									print("date c")
# 									print(date_c)
# 									date_a = datetime.strptime(d_a, '%Y-%m-%d %H:%M:%S') - timedelta(days=25)
# 									date_b = datetime.strptime(d_s, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)
# 									date_c = datetime.strptime(d_c, '%Y-%m-%d %H:%M:%S')
# 									#if date_c >= date_a and date_c <= date_b:
# 									res = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
# 									biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check Out'""", 
# 									(users, str(date), check_out))
# 									if res:
# 										# frappe.db.set_value("Attendance Logs", res[0][0], "biometric_id", res[0][1])
# 										# frappe.db.set_value("Attendance Logs", res[0][0], "ip", '115.167.64.233')
# 										atl = frappe.get_doc("Attendance Logs",res[0][0])
# 										atl.save()
# 									else:
# 										print("adding check out")
# 										doc2 = frappe.new_doc("Attendance Logs")
# 										doc2.attendance = check_out_string
# 										doc2.biometric_id= users
# 										doc2.attendance_date= str(date)
# 										doc2.attendance_time= str(check_out)
# 										doc2.type = "Check Out"
# 										doc2.ip = '115.167.64.233:4370'
# 										doc2.save()
# 						except:
# 							frappe.log_error(frappe.get_traceback(),"Attendance hook test")
# 				f = open("/home/frappe/frappe-bench/attendance.json", "a")
# 				f.write(json.dumps(str(attendance)))
# 				f.close()
# 				settle_night_s()
# 				print(len(attendance))
# 	except:
# 		print ("Process terminate : {}"+frappe.get_traceback())


# @frappe.whitelist()
# def get_attendance_from_api(date):
# 	response = request(method="GET", url="""https://api.ubiattendance.com/attendanceservice/getempattendance?apikey==AlVGhUVup0cNFjWadVb4xmVwolNZpmTXJmVKJnUrRWYWZFcHZVMotmVrlTUTxmWOJ1MCl1VrZ1dWdlRzpVRax2VtJ1RWJDdPFWMWhlVtRHbW1GaHlFM4gXTHZEWWtmWXVlaGVVVB1TP&Attendancedate={0} 
# 		""".format(date))
# 	response.raise_for_status()
# 	data = json.loads(response.text.split("]")[0]+"]")
# 	for item in data:
# 		chk_in = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
# 			biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check In'""", 
# 									(item["Employeecode"], item["attendancedate"], item["Timein"]))
# 		if not chk_in:
# 			#add checkin
# 			checkin = frappe.new_doc("Attendance Logs")
# 			checkin.attendance = "&lt;Attendance&gt;: {0} : {1} {2} (1, 1)".format(item["Employeecode"],item["attendancedate"],item["Timein"])
# 			checkin.biometric_id= item["Employeecode"]
# 			checkin.attendance_date= item["attendancedate"]
# 			checkin.attendance_time= item["Timein"]
# 			checkin.type = "Check In"
# 			checkin.ip = 'from_rest_api'
# 			checkin.save()

# 		else:
# 			doc = frappe.get_doc("Attendance Logs",chk_in[0][0])
# 			doc.attendance = "&lt;Attendance&gt;: {0} : {1} {2} (1, 1)".format(item["Employeecode"],item["attendancedate"],item["Timein"])
# 			doc.biometric_id= item["Employeecode"]
# 			doc.attendance_date= item["attendancedate"]
# 			doc.attendance_time= item["Timein"]
# 			doc.type = "Check In"
# 			doc.ip = 'from_rest_api'
# 			doc.save()



# 		chk_out = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
# 									biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check Out'""", 
# 									(item["Employeecode"], item["attendancedate"], item["Timeout"]))
# 		if not chk_out:
# 			#add chkout
# 			chkout = frappe.new_doc("Attendance Logs")
# 			chkout.biometric_id= item["Employeecode"]
# 			chkout.attendance = "&lt;Attendance&gt;: {0} : {1} {2} (1, 1)".format(item["Employeecode"],item["attendancedate"],item["Timeout"])
# 			chkout.attendance_date= item["attendancedate"]
# 			chkout.attendance_time= item["Timeout"]
# 			chkout.type = "Check Out"
# 			chkout.ip = 'from_rest_api'
# 			chkout.save()

# 		else:
# 			doc = frappe.get_doc("Attendance Logs",chk_out[0][0])
# 			doc.attendance = "&lt;Attendance&gt;: {0} : {1} {2} (1, 1)".format(item["Employeecode"],item["attendancedate"],item["Timeout"])
# 			doc.biometric_id= item["Employeecode"]
# 			doc.attendance_date= item["attendancedate"]
# 			doc.attendance_time= item["Timeout"]
# 			doc.type = "Check Out"
# 			doc.ip = 'from_rest_api'
# 			doc.save()

# 	return "done"
		

# @frappe.whitelist()
# def get_attendance_from_hook():
# 	# config  = frappe.get_single("Attendance Time Set")
# 	# frappe.log_error(str(get_datetime().time())+" "+str(get_datetime(config.daily_sync_time).time()),"BGHOOK")
# 	# if getdate(config.last_sync_date) < getdate(today()) and get_datetime(config.daily_sync_time).time() <= get_datetime().time():
# 	args={
# 		"from_date":getdate(today()),
# 		"to_date":getdate(today()),
# 	}
# 	# config.last_sync_date = getdate(today())
# 	# config.save()
# 	get_attendance_long(**args)



# @frappe.whitelist()
# def email_report():
# 		from frappe.email.doctype.auto_email_report.auto_email_report import send_now
# 		auto_email_report = frappe.get_doc('Auto Email Report', "Daily Attendance")
# 		auto_email_report.update({
# 			"filters": """{."from.":\""""+str(getdate(today()))+"""\",\"to\":\""""+str(getdate(today()))+"""\"}"""
# 		})
# 		auto_email_report.save()
# 		send_now("Daily Attendance")

	