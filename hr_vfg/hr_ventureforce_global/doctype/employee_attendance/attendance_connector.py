from __future__ import unicode_literals
import frappe
from frappe import utils
from frappe import throw, _

import sys
import time
from zk import ZK, const
from datetime import datetime, timedelta
from frappe.utils import date_diff, add_months, get_datetime, today, getdate, add_days, flt, get_last_day
import calendar
from frappe.utils.background_jobs import enqueue
from requests import request
import json
from datetime import datetime
from datetime import timedelta


@frappe.whitelist()
def get_attendance_long(**args):
	if not args:
		args = frappe.local.form_dict
	"Enqueue longjob for taking backup to dropbox"
	enqueue("hr_vfg.hr_ventureforce_global.doctype.employee_attendance.attendance_connector.execute_job", 
	 queue='long', timeout=8000,args=args)
	
	frappe.msgprint(_("Queued for biometric attendance. It may take a few minutes to an hour."))
@frappe.whitelist()
def execute_job(args):
	hr_settings = frappe.get_single('V HR Settings')
	for machine in hr_settings.attendance_machine:
		if machine.type == 'In':
			get_checkins(args,machine.ip,machine.port,machine.password)
		elif machine.type == "Out":
			get_checkouts(args,machine.ip,machine.port,machine.password)
		else:
			get_checkins_checkouts(args,machine.ip,machine.port,machine.password)

def get_checkins(args=None, ip=None, port=None,password=0):
	conn = None
	if not args:
		args = {"from_date":"2022-01-01","to_date":today()}
	emp_list = [] #110.93.236.48
	if not password:
		password = 0
	zk = ZK(ip, port=int(port), timeout=1500, password=password, force_udp=False, ommit_ping=False)
	frappe.log_error("Starting in..","Attendance hook test")
	try:
		conn = zk.connect()
		if conn:
			users = conn.get_users()
			if users:
				for u in users:
					#print(u)
					pass

			attendance = conn.get_attendance()
			print("getting attendance data")
			
			if attendance:
				#print(attendance)
				
				attendance_dict={}
				condition1 =""
				condition2=""
				biometric_list=[]
				b_filters = {}
				if args.get("employee"):
					condition1=" and parent in (select name from `tabEmployee Attendance` where employee='{0}')".format(args.get("employee"))
					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where name='{0}')".format(args.get("employee"))
					b_filters["name"]=args.get("employee")
				if args.get("department"):
					condition1=" and parent in (select name from `tabEmployee Attendance` where department='{0}')".format(args.get("department"))
					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where department='{0}')".format(args.get("department"))
					b_filters["department"]=args.get("department")
				if args.get("employee") and args.get("department"):
					condition1=" and parent in (select name from `tabEmployee Attendance` where employee='{0}' and department='{1}')".format(args.get("employee"),args.get("department"))
					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where name='{0}' and department='{1}')".format(args.get("employee"),args.get("department"))

				B_r = frappe.db.get_all("Employee",filters=b_filters,fields=["biometric_id"])
				for bid in B_r:
					biometric_list.append(bid.biometric_id)
				frappe.db.sql(""" delete from `tabAttendance Logs` where attendance_date >= %s and attendance_date <= %s and ip=%s {0} """.format(condition2), (args.get("from_date"),args.get("to_date"),ip+":"+port))
				frappe.db.sql(""" update `tabEmployee Attendance Table` set check_in_1=NULL,  late_sitting=NULL, night_switch=0 where date >= %s and date <= %s and ip=%s and type!="Adjustment"{0} """.format(condition1), (args.get("from_date"),args.get("to_date"),ip+":"+port))
				frappe.db.commit()
				print(str(biometric_list))
				#frappe.log_error(len(attendance))
				for attend1 in attendance:
					if getdate(str(attend1).split()[3]) < getdate(args.get("from_date")) or getdate(str(attend1).split()[3]) > getdate(args.get("to_date")):
						continue
					# if str(attend1).split()[1] == "405":
					# 		print("Found 1 a")
					if len(biometric_list) > 0:
						if str(attend1).split()[1] not in biometric_list:
							continue
					if attendance_dict.get(str(attend1).split()[1]):
						if attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3]):
							# attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3])["check in"]=str(attend1).split()[4]
							# attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3])["checkin string"]=str(attend1)
							pass
						else:
							attendance_dict.get(str(attend1).split()[1])[str(attend1).split()[3]]={
								"check in": str(attend1).split()[4],
								"checkin string":str(attend1)
							}
					else:
						attendance_dict[str(attend1).split()[1]]={
							str(attend1).split()[3] :{
								"check in": str(attend1).split()[4],
								"checkin string":str(attend1)
							}
						}
					
					

				import json
				for users in attendance_dict:
					print(users)
					for dates in attendance_dict[users]:
						try:
							date = dates
							check_in = attendance_dict[users][dates].get("check in")
							check_in_string = attendance_dict[users][dates].get("checkin string")
							
							if check_in:
									d_a = str(utils.today()) +" 8:30:0"
									d_b = str(utils.today()) +" 1:0:0"
									d_s = str(utils.today()) +" 23:59:00"
									d_c = str(date+" "+check_in)
									
									res = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
									biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check In'""", 
									(users, str(date), check_in))
									if res:
										
										atl = frappe.get_doc("Attendance Logs",res[0][0])
										atl.save()
									else:
										print("adding check in")
										doc1 = frappe.new_doc("Attendance Logs")
										doc1.attendance = check_in_string
										doc1.biometric_id= users
										doc1.attendance_date= str(date)
										doc1.attendance_time= str(check_in)
										doc1.type = "Check In"
										doc1.ip = ip+":"+port
										doc1.save()
							
						except:
							frappe.log_error(frappe.get_traceback(),"Attendance hook test")
				
	except Exception as e:
		print ("Process terminate : {}"+frappe.get_traceback())
		frappe.log_error(frappe.get_traceback(),"Attendance hook test")
	finally:
		if conn:
			conn.disconnect()

def check_time(attend1):
	t_biometric = str(attend1).split()[1]
	flg = False
	t_date = str(attend1).split()[3]
	employee = frappe.db.get_value("Employee",{"biometric_id":t_biometric},"name")
	shift_ass = frappe.get_all("Shift Assignment", filters={'employee': employee,
													'start_date': ["<=", getdate(t_date)],'end_date': [">=", getdate(t_date)]}, fields=["*"])
	if len(shift_ass) > 0:
		shift = shift_ass[0].shift_type
	else:
		shift_ass = frappe.get_all("Shift Assignment", filters={'employee': employee,
															'start_date': ["<=", getdate(t_date)]}, fields=["*"])
	if len(shift_ass) > 0:
			shift = shift_ass[0].shift_type
			shift_doc = frappe.get_doc("Shift Type", shift)
			s_type = shift_doc.shift_type
			t_check_out = str(attend1).split()[4]
			t_check_out_f_f = timedelta(hours=int(t_check_out.split(":")[0]),minutes=int(t_check_out.split(":")[1]))
			shift_start_t = timedelta(hours=int(str(shift_doc.start_time).split(":")[0]),minutes=int(str(shift_doc.start_time).split(":")[1]))
			if t_check_out_f_f < shift_start_t:
				prev_date = add_days(getdate(t_date),-1)
				return True, prev_date
			return True, False

	return False, False
def get_checkouts(args=None,ip=None, port=None,password=0):
	conn = None
	emp_list = [] #110.93.236.48
	if not args:
		args = {"from_date":"2023-03-01","to_date":today()}
	if not password:
		password = 0
	zk = ZK(ip, port=int(port), timeout=1500, password=password, force_udp=False, ommit_ping=False)
	frappe.log_error("Starting out now","Attendance hook test")
	try:
		conn = zk.connect()
		if conn:
			users = conn.get_users()
			if users:
				for u in users:
					#print(u)
					pass

			attendance = conn.get_attendance()
			print("getting attendance data")
			#print(attendance)
			if attendance:
				#print(attendance)
				
				attendance_dict={}
				condition1 =""
				condition2=""
				biometric_list=[]
				b_filters = {}
				if args.get("employee"):
					condition1=" and parent in (select name from `tabEmployee Attendance` where employee='{0}')".format(args.get("employee"))
					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where name='{0}')".format(args.get("employee"))
					b_filters["name"]=args.get("employee")
				if args.get("department"):
					condition1=" and parent in (select name from `tabEmployee Attendance` where department='{0}')".format(args.get("department"))
					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where department='{0}')".format(args.get("department"))
					b_filters["department"]=args.get("department")
				if args.get("employee") and args.get("department"):
					condition1=" and parent in (select name from `tabEmployee Attendance` where employee='{0}' and department='{1}')".format(args.get("employee"),args.get("department"))
					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where name='{0}' and department='{1}')".format(args.get("employee"),args.get("department"))

				B_r = frappe.db.get_all("Employee",filters=b_filters,fields=["biometric_id"])
				for bid in B_r:
					biometric_list.append(bid.biometric_id)
				frappe.db.sql(""" delete from `tabAttendance Logs` where attendance_date >= %s and attendance_date <= %s and ip=%s {0} """.format(condition2), (args.get("from_date"),args.get("to_date"),ip+":"+port))
				frappe.db.sql(""" update `tabEmployee Attendance Table` set check_out_1=NULL, late_sitting=NULL, night_switch=0 where date >= %s and date <= %s and ip=%s and type!="Adjustment"{0} """.format(condition1), (args.get("from_date"),args.get("to_date"),ip+":"+port))
				frappe.db.commit()
				for attend1 in attendance:
					if getdate(str(attend1).split()[3]) < getdate(args.get("from_date")) or getdate(str(attend1).split()[3]) > getdate(args.get("to_date")):
						continue
					if len(biometric_list) > 0:
						if str(attend1).split()[1] not in biometric_list:
							continue
					if attendance_dict.get(str(attend1).split()[1]):
						if attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3]):
							shift, prev_date = check_time(attend1)
							if shift:
									if prev_date:
										if attendance_dict.get(str(attend1).split()[1]).get(str(prev_date)):
											attendance_dict.get(str(attend1).split()[1]).get(str(prev_date))["check out"]=str(attend1).split()[4]
											attendance_dict.get(str(attend1).split()[1]).get(str(prev_date))["checkout string"]=str(attend1)
										else:
											attendance_dict[str(attend1).split()[1]]={
												str(prev_date) :{
													"check out": str(attend1).split()[4],
													"checkout string":str(attend1)
												}
											}
									else:
										flg = True

							else: 
								flg = True
							
							if flg:
								attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3])["check out"]=str(attend1).split()[4]
								attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3])["checkout string"]=str(attend1)
							print("done")
						else:
							shift, prev_date = check_time(attend1)
							if prev_date:
								attendance_dict.get(str(attend1).split()[1])[str(prev_date)]={
									"check out": str(attend1).split()[4],
									"checkout string":str(attend1)
								}
							else:
								attendance_dict.get(str(attend1).split()[1])[str(attend1).split()[3]]={
									"check out": str(attend1).split()[4],
									"checkout string":str(attend1)
								}
					else:
						
						shift, prev_date = check_time(attend1)
						if prev_date:
							attendance_dict[str(attend1).split()[1]]={
								str(prev_date) :{
									"check out": str(attend1).split()[4],
									"checkout string":str(attend1)
								}
							}
						else:
							attendance_dict[str(attend1).split()[1]]={
								str(attend1).split()[3] :{
									"check out": str(attend1).split()[4],
									"checkout string":str(attend1)
								}
							}
					
					

				import json
				#print(attendance_dict)
				for users in attendance_dict:
					print(users)
					for dates in attendance_dict[users]:
						try:
							date = dates
							check_in = attendance_dict[users][dates].get("check in")
							check_in_string = attendance_dict[users][dates].get("checkin string")
							check_out = attendance_dict[users][dates].get("check out")
							check_out_string = attendance_dict[users][dates].get("checkout string")
							
							check_in = None
							temp_chk_in = None
							
							if check_out:
									
									if check_in:
										x = datetime.strptime(
                        					str(temp_chk_in), '%H:%M:%S').time()
										y = datetime.strptime(
                        					str(check_out), '%H:%M:%S').time()
										hi,mi,si = str(x).split(':')
										ho,mo,so = str(y).split(':')
										diff_time = timedelta(hours=0, minutes=30, seconds=0)
										
										if (timedelta(hours=float(ho), minutes=float(mo), seconds=float(so))-timedelta(hours=float(hi), minutes=float(mi), seconds=float(si))) < diff_time:
											continue

									res = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
									biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check Out'""", 
									(users, str(date), check_out))
									if res:
										
										atl = frappe.get_doc("Attendance Logs",res[0][0])
										atl.save()
									else:
										print("adding check out")
										doc2 = frappe.new_doc("Attendance Logs")
										doc2.attendance = check_out_string
										doc2.biometric_id= users
										doc2.attendance_date= str(date)
										doc2.attendance_time= str(check_out)
										doc2.type = "Check Out"
										doc2.ip = '182.184.121.132:4371'
										doc2.save()
						except:
							frappe.log_error(frappe.get_traceback(),"Attendance hook test")
				
				
	except Exception as e:
		frappe.log_error ("Process terminate : {}"+frappe.get_traceback())
	finally:
		if conn:
			conn.disconnect()


def get_checkins_checkouts(args=None,ip=None, port=None,password=0):
	conn = None
	emp_list = [] #110.93.236.48
	if not args:
		args = {"from_date":"2023-03-01","to_date":today()}
	if not password:
		password = 0
	zk = ZK(ip, port=int(port), timeout=1500, password=password, force_udp=False, ommit_ping=False)
	frappe.log_error("Starting in/out..","Attendance hook test")
	try:
		conn = zk.connect()
		if conn:
			users = conn.get_users()
			if users:
				for u in users:
					#print(u)
					pass

			attendance = conn.get_attendance()
			print("getting attendance data")
			#print(attendance)
			if attendance:
				#print(attendance)
				
				attendance_dict={}
				condition1 =""
				condition2=""
				biometric_list=[]
				b_filters = {}
				if args.get("employee"):
					condition1=" and parent in (select name from `tabEmployee Attendance` where employee='{0}')".format(args.get("employee"))
					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where name='{0}')".format(args.get("employee"))
					b_filters["name"]=args.get("employee")
				if args.get("department"):
					condition1=" and parent in (select name from `tabEmployee Attendance` where department='{0}')".format(args.get("department"))
					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where department='{0}')".format(args.get("department"))
					b_filters["department"]=args.get("department")
				if args.get("employee") and args.get("department"):
					condition1=" and parent in (select name from `tabEmployee Attendance` where employee='{0}' and department='{1}')".format(args.get("employee"),args.get("department"))
					condition2=" and biometric_id in (select biometric_id from `tabEmployee` where name='{0}' and department='{1}')".format(args.get("employee"),args.get("department"))

				B_r = frappe.db.get_all("Employee",filters=b_filters,fields=["biometric_id"])
				for bid in B_r:
					biometric_list.append(bid.biometric_id)
				frappe.db.sql(""" delete from `tabAttendance Logs` where attendance_date >= %s and attendance_date <= %s and ip=%s {0} """.format(condition2), (args.get("from_date"),args.get("to_date"),ip+":"+port))
				frappe.db.sql(""" update `tabEmployee Attendance Table` set check_in_1 = NULL, check_out_1=NULL, late_sitting=NULL, night_switch=0 where date >= %s and date <= %s and ip=%s and type!="Adjustment"{0} """.format(condition1), (args.get("from_date"),args.get("to_date"),ip+":"+port))
				frappe.db.commit()
				for attend1 in attendance:
					if getdate(str(attend1).split()[3]) < getdate(args.get("from_date")) or getdate(str(attend1).split()[3]) > getdate(args.get("to_date")):
						continue
					if len(biometric_list) > 0:
						if str(attend1).split()[1] not in biometric_list:
							continue
					if attendance_dict.get(str(attend1).split()[1]):
						if attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3]):
							t_biometric = str(attend1).split()[1]
							flg = False
							t_date = str(attend1).split()[3]
							employee = frappe.db.get_value("Employee",{"biometric_id":t_biometric},"name")
							shift_ass = frappe.get_all("Shift Assignment", filters={'employee': employee,
                                                                            'start_date': ["<=", getdate(t_date)],'end_date': [">=", getdate(t_date)]}, fields=["*"])
							if len(shift_ass) > 0:
								shift = shift_ass[0].shift_type
							else:
								shift_ass = frappe.get_all("Shift Assignment", filters={'employee': employee,
																					'start_date': ["<=", getdate(t_date)]}, fields=["*"])
							if len(shift_ass) > 0:
									shift = shift_ass[0].shift_type
									shift_doc = frappe.get_doc("Shift Type", shift)
									s_type = shift_doc.shift_type
									t_check_out = str(attend1).split()[4]
									t_check_out_f_f = timedelta(hours=int(t_check_out.split(":")[0]),minutes=int(t_check_out.split(":")[1]))
									shift_start_t = timedelta(hours=int(str(shift_doc.start_time).split(":")[0]),minutes=int(str(shift_doc.start_time).split(":")[1]))
									if t_check_out_f_f < shift_start_t:
										prev_date = add_days(getdate(t_date),-1)
										if attendance_dict.get(str(attend1).split()[1]).get(str(prev_date)):
											attendance_dict.get(str(attend1).split()[1]).get(str(prev_date))["check out"]=str(attend1).split()[4]
											attendance_dict.get(str(attend1).split()[1]).get(str(prev_date))["checkout string"]=str(attend1)
										else:
											attendance_dict[str(attend1).split()[1]]={
												str(prev_date) :{
													"check out": str(attend1).split()[4],
													"checkout string":str(attend1)
												}
											}
									else:
										flg = True

							else: 
								flg = True
							
							if flg:
								attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3])["check out"]=str(attend1).split()[4]
								attendance_dict.get(str(attend1).split()[1]).get(str(attend1).split()[3])["checkout string"]=str(attend1)
							print("done")
						else:
							attendance_dict.get(str(attend1).split()[1])[str(attend1).split()[3]]={
								"check in": str(attend1).split()[4],
								"checkin string":str(attend1)
							}
					else:
						attendance_dict[str(attend1).split()[1]]={
							str(attend1).split()[3] :{
								"check in": str(attend1).split()[4],
								"checkin string":str(attend1)
							}
						}
					
					

				import json
				#print(attendance_dict)
				for users in attendance_dict:
					print(users)
					for dates in attendance_dict[users]:
						try:
							date = dates
							check_in = attendance_dict[users][dates].get("check in")
							check_in_string = attendance_dict[users][dates].get("checkin string")
							check_out = attendance_dict[users][dates].get("check out")
							check_out_string = attendance_dict[users][dates].get("checkout string")
							
							if check_in:
									d_a = str(utils.today()) +" 8:30:0"
									d_b = str(utils.today()) +" 1:0:0"
									d_s = str(utils.today()) +" 23:59:00"
									d_c = str(date+" "+check_in)
									temp_chk_in = check_in

									res = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
									biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check In'""", 
									(users, str(date), check_in))
									if res:
										
										atl = frappe.get_doc("Attendance Logs",res[0][0])
										atl.save()
									else:
										print("adding check in")
										doc1 = frappe.new_doc("Attendance Logs")
										doc1.attendance = check_in_string
										doc1.biometric_id= users
										doc1.attendance_date= str(date)
										doc1.attendance_time= str(check_in)
										doc1.type = "Check In"
										doc1.ip = ip+":"+port
										doc1.save()
							if check_out:
									
									if check_in:
										x = datetime.strptime(
                        					str(temp_chk_in), '%H:%M:%S').time()
										y = datetime.strptime(
                        					str(check_out), '%H:%M:%S').time()
										hi,mi,si = str(x).split(':')
										ho,mo,so = str(y).split(':')
										diff_time = timedelta(hours=0, minutes=30, seconds=0)
										
										if (timedelta(hours=float(ho), minutes=float(mo), seconds=float(so))-timedelta(hours=float(hi), minutes=float(mi), seconds=float(si))) < diff_time:
											continue

									
									d_a = str(utils.today()) +" 8:30:0"
									d_b = str(utils.today()) +" 1:0:0"
									d_s = str(utils.today()) +" 23:59:00"
									d_c = str(date+" "+check_out)

									res = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
									biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check Out'""", 
									(users, str(date), check_out))
									if res:
										
										atl = frappe.get_doc("Attendance Logs",res[0][0])
										atl.save()
									else:
										print("adding check out")
										doc2 = frappe.new_doc("Attendance Logs")
										doc2.attendance = check_out_string
										doc2.biometric_id= users
										doc2.attendance_date= str(date)
										doc2.attendance_time= str(check_out)
										doc2.type = "Check Out"
										doc2.ip = ip+":"+port
										doc2.save()
						except:
							frappe.log_error(frappe.get_traceback(),"Attendance hook test")
				
				
	except Exception as e:
		print ("Process terminate : {}"+frappe.get_traceback())
	finally:
		if conn:
			conn.disconnect()


@frappe.whitelist()
def get_attendance_from_api(date):
	response = request(method="GET", url="""https://api.ubiattendance.com/attendanceservice/getempattendance?apikey==AlVGhUVup0cNFjWadVb4xmVwolNZpmTXJmVKJnUrRWYWZFcHZVMotmVrlTUTxmWOJ1MCl1VrZ1dWdlRzpVRax2VtJ1RWJDdPFWMWhlVtRHbW1GaHlFM4gXTHZEWWtmWXVlaGVVVB1TP&Attendancedate={0} 
		""".format(date))
	response.raise_for_status()
	data = json.loads(response.text.split("]")[0]+"]")
	for item in data:
		chk_in = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
			biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check In'""", 
									(item["Employeecode"], item["attendancedate"], item["Timein"]))
		if not chk_in:
			#add checkin
			checkin = frappe.new_doc("Attendance Logs")
			checkin.attendance = "&lt;Attendance&gt;: {0} : {1} {2} (1, 1)".format(item["Employeecode"],item["attendancedate"],item["Timein"])
			checkin.biometric_id= item["Employeecode"]
			checkin.attendance_date= item["attendancedate"]
			checkin.attendance_time= item["Timein"]
			checkin.type = "Check In"
			checkin.ip = 'from_rest_api'
			checkin.save()

		else:
			doc = frappe.get_doc("Attendance Logs",chk_in[0][0])
			doc.attendance = "&lt;Attendance&gt;: {0} : {1} {2} (1, 1)".format(item["Employeecode"],item["attendancedate"],item["Timein"])
			doc.biometric_id= item["Employeecode"]
			doc.attendance_date= item["attendancedate"]
			doc.attendance_time= item["Timein"]
			doc.type = "Check In"
			doc.ip = 'from_rest_api'
			doc.save()



		chk_out = frappe.db.sql(""" select name, biometric_id from `tabAttendance Logs` where 
									biometric_id=%s and attendance_date=%s and attendance_time=%s and type='Check Out'""", 
									(item["Employeecode"], item["attendancedate"], item["Timeout"]))
		if not chk_out:
			#add chkout
			chkout = frappe.new_doc("Attendance Logs")
			chkout.biometric_id= item["Employeecode"]
			chkout.attendance = "&lt;Attendance&gt;: {0} : {1} {2} (1, 1)".format(item["Employeecode"],item["attendancedate"],item["Timeout"])
			chkout.attendance_date= item["attendancedate"]
			chkout.attendance_time= item["Timeout"]
			chkout.type = "Check Out"
			chkout.ip = 'from_rest_api'
			chkout.save()

		else:
			doc = frappe.get_doc("Attendance Logs",chk_out[0][0])
			doc.attendance = "&lt;Attendance&gt;: {0} : {1} {2} (1, 1)".format(item["Employeecode"],item["attendancedate"],item["Timeout"])
			doc.biometric_id= item["Employeecode"]
			doc.attendance_date= item["attendancedate"]
			doc.attendance_time= item["Timeout"]
			doc.type = "Check Out"
			doc.ip = 'from_rest_api'
			doc.save()

	return "done"
		

@frappe.whitelist()
def get_attendance_from_hook():
	frappe.log_error("Fetchhing","BGHOOK")
	args={
		"from_date":add_days(today(),-1),
		"to_date":getdate(today()),
	}
	get_attendance_long(**args)


@frappe.whitelist()
def email_report():
		from frappe.email.doctype.auto_email_report.auto_email_report import send_now
		auto_email_report = frappe.get_doc('Auto Email Report', "Daily Attendance")
		auto_email_report.update({
			"filters": """{."from.":\""""+str(getdate(today()))+"""\",\"to\":\""""+str(getdate(today()))+"""\"}"""
		})
		auto_email_report.save()
		send_now("Daily Attendance")

	