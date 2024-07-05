# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe import msgprint, _
from datetime import datetime
from datetime import timedelta
import time
from erpnext.hr.utils import get_holidays_for_employee
from frappe.utils import cstr, flt


class EmployeeAttendance(Document):
    def autoname(self):
        self.name = make_autoname(self.employee + '-' + self.month)

    def validate(self):
        total_early = 0
        total_lates = 0
        total_half_days = 0
        total_hr_worked = timedelta(hours=0, minutes=0, seconds=0)
        total_per_day_h = timedelta(hours=0, minutes=0, seconds=0)
        total_late_hr_worked = timedelta(hours=0, minutes=0, seconds=0)
        required_working_hrs = 0.0
        total_absents = 0
        holiday_doc = None
        half_day_leave = None
        self.no_of_nights = 0
        
        for ii in range(len(self.table1)):
           
            tempdate = datetime.strptime(
                        str(self.table1[ii].date), '%Y-%m-%d')
            if self.table1[ii].date in get_holidays_for_employee(self.employee,tempdate,tempdate):
                        #frappe.msgprint(str(day_name))
                        continue
            #try:
            LA = frappe.get_all("Leave Application", filters={"from_date":["<=",tempdate],"to_date":[">=",tempdate]},fields=["*"])
            if len(LA) > 0:
                if LA[0].half_day:
                    half_day_leave = 1
                else:
                    continue

            # except:
            #     pass
            try:
                total_time = timedelta(hours=0, minutes=0, seconds=0)
                hrs = timedelta(hours=0, minutes=0, seconds=0)
                #s3 = time.strftime("%H:%M:%S", time.gmtime(diff))
                if self.table1[ii].check_in_1 and self.table1[ii].check_out_1:
                    x = datetime.strptime(
                        str(self.table1[ii].check_in_1), '%H:%M:%S').time()
                    y = datetime.strptime(
                        str(self.table1[ii].check_out_1), '%H:%M:%S').time()
                    xh, xm, xs = str(x).split(":")
                    yh, ym, ys = str(y).split(":")
                    # xz = int(xh)*3600+int(xm)*60+int(xs)*1
                    # yz = int(yh)*3600+int(ym)*60+int(ys)*1
                    # total_time = total_time + abs(yz - xz)
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
                    total_time = total_time + diff
                if self.table1[ii].check_in_2 and self.table1[ii].check_out_2:
                    x = datetime.strptime(
                        str(self.table1[ii].check_in_2), '%H:%M:%S').time()
                    y = datetime.strptime(
                        str(self.table1[ii].check_out_2), '%H:%M:%S').time()
                    xh, xm, xs = str(x).split(":")
                    yh, ym, ys = str(y).split(":")
                    in_time = timedelta(hours=float(
                        xh), minutes=float(xm), seconds=float(xs))
                    out_time = timedelta(hours=float(
                        yh), minutes=float(ym), seconds=float(ys))
                    diff = str(out_time - in_time)
                    if "day" in diff:
                        diff = diff.split("day, ")[1].split(":")
                        diff = timedelta(hours=float(diff[0]), minutes=float(
                            diff[1]), seconds=float(diff[2]))
                    else:
                        diff = out_time - in_time
                    total_time = total_time + diff
                if self.table1[ii].check_in_3 and self.table1[ii].check_out_3:
                    x = datetime.strptime(
                        str(self.table1[ii].check_in_3), '%H:%M:%S').time()
                    y = datetime.strptime(
                        str(self.table1[ii].check_out_3), '%H:%M:%S').time()
                    xh, xm, xs = str(x).split(":")
                    yh, ym, ys = str(y).split(":")
                    in_time = timedelta(hours=float(
                        xh), minutes=float(xm), seconds=float(xs))
                    out_time = timedelta(hours=float(
                        yh), minutes=float(ym), seconds=float(ys))
                    diff = str(out_time - in_time)
                    if "day" in diff:
                        diff = diff.split("day, ")[1].split(":")
                        diff = timedelta(hours=float(diff[0]), minutes=float(
                            diff[1]), seconds=float(diff[2]))
                    else:
                        diff = out_time - in_time
                    total_time = total_time + diff
                if self.table1[ii].check_in_4 and self.table1[ii].check_out_4:
                    x = datetime.strptime(
                        str(self.table1[ii].check_in_4), '%H:%M:%S').time()
                    y = datetime.strptime(
                        str(self.table1[ii].check_out_4), '%H:%M:%S').time()
                    xh, xm, xs = str(x).split(":")
                    yh, ym, ys = str(y).split(":")
                    in_time = timedelta(hours=float(
                        xh), minutes=float(xm), seconds=float(xs))
                    out_time = timedelta(hours=float(
                        yh), minutes=float(ym), seconds=float(ys))
                    diff = str(out_time - in_time)
                    if "day" in diff:
                        diff = diff.split("day, ")[1].split(":")
                        diff = timedelta(hours=float(diff[0]), minutes=float(
                            diff[1]), seconds=float(diff[2]))
                    else:
                        diff = out_time - in_time
                    total_time = total_time + diff
                if self.table1[ii].check_in_5 and self.table1[ii].check_out_5:
                    x = datetime.strptime(
                        str(self.table1[ii].check_in_5), '%H:%M:%S').time()
                    y = datetime.strptime(
                        str(self.table1[ii].check_out_5), '%H:%M:%S').time()
                    xh, xm, xs = str(x).split(":")
                    yh, ym, ys = str(y).split(":")
                    in_time = timedelta(hours=float(
                        xh), minutes=float(xm), seconds=float(xs))
                    out_time = timedelta(hours=float(
                        yh), minutes=float(ym), seconds=float(ys))
                    diff = str(out_time - in_time)
                    if "day" in diff:
                        diff = diff.split("day, ")[1].split(":")
                        diff = timedelta(hours=float(diff[0]), minutes=float(
                            diff[1]), seconds=float(diff[2]))
                    else:
                        diff = out_time - in_time
                    total_time = total_time + diff
                if self.table1[ii].check_in_6 and self.table1[ii].check_out_6:
                    x = datetime.strptime(
                        str(self.table1[ii].check_in_6), '%H:%M:%S').time()
                    y = datetime.strptime(
                        str(self.table1[ii].check_out_6), '%H:%M:%S').time()
                    xh, xm, xs = str(x).split(":")
                    yh, ym, ys = str(y).split(":")
                    in_time = timedelta(hours=float(
                        xh), minutes=float(xm), seconds=float(xs))
                    out_time = timedelta(hours=float(
                        yh), minutes=float(ym), seconds=float(ys))
                    diff = str(out_time - in_time)
                    if "day" in diff:
                        diff = diff.split("day, ")[1].split(":")
                        diff = timedelta(hours=float(diff[0]), minutes=float(
                            diff[1]), seconds=float(diff[2]))
                    else:
                        diff = out_time - in_time
                    total_time = total_time + diff
                if self.table1[ii].check_in_7 and self.table1[ii].check_out_7:
                    x = datetime.strptime(
                        str(self.table1[ii].check_in_7), '%H:%M:%S').time()
                    y = datetime.strptime(
                        str(self.table1[ii].check_out_7), '%H:%M:%S').time()
                    xh, xm, xs = str(x).split(":")
                    yh, ym, ys = str(y).split(":")
                    in_time = timedelta(hours=float(
                        xh), minutes=float(xm), seconds=float(xs))
                    out_time = timedelta(hours=float(
                        yh), minutes=float(ym), seconds=float(ys))
                    diff = str(out_time - in_time)
                    if "day" in diff:
                        diff = diff.split("day, ")[1].split(":")
                        diff = timedelta(hours=float(diff[0]), minutes=float(
                            diff[1]), seconds=float(diff[2]))
                    else:
                        diff = out_time - in_time
                    total_time = total_time + diff
                if self.table1[ii].check_in_8 and self.table1[ii].check_out_8:
                    x = datetime.strptime(
                        str(self.table1[ii].check_in_8), '%H:%M:%S').time()
                    y = datetime.strptime(
                        str(self.table1[ii].check_out_8), '%H:%M:%S').time()
                    xh, xm, xs = str(x).split(":")
                    yh, ym, ys = str(y).split(":")
                    in_time = timedelta(hours=float(
                        xh), minutes=float(xm), seconds=float(xs))
                    out_time = timedelta(hours=float(
                        yh), minutes=float(ym), seconds=float(ys))
                    diff = str(out_time - in_time)
                    if "day" in diff:
                        diff = diff.split("day, ")[1].split(":")
                        diff = timedelta(hours=float(diff[0]), minutes=float(
                            diff[1]), seconds=float(diff[2]))
                    else:
                        diff = out_time - in_time
                    total_time = total_time + diff
                if self.table1[ii].check_in_9 and self.table1[ii].check_out_9:
                    x = datetime.strptime(
                        str(self.table1[ii].check_in_9), '%H:%M:%S').time()
                    y = datetime.strptime(
                        str(self.table1[ii].check_out_9), '%H:%M:%S').time()
                    xh, xm, xs = str(x).split(":")
                    yh, ym, ys = str(y).split(":")
                    in_time = timedelta(hours=float(
                        xh), minutes=float(xm), seconds=float(xs))
                    out_time = timedelta(hours=float(
                        yh), minutes=float(ym), seconds=float(ys))
                    diff = str(out_time - in_time)
                    if "day" in diff:
                        diff = diff.split("day, ")[1].split(":")
                        diff = timedelta(hours=float(diff[0]), minutes=float(
                            diff[1]), seconds=float(diff[2]))
                    else:
                        diff = out_time - in_time
                    total_time = total_time + diff
                if self.table1[ii].check_in_10 and self.table1[ii].check_out_10:
                    x = datetime.strptime(
                        str(self.table1[ii].check_in_10), '%H:%M:%S').time()
                    y = datetime.strptime(
                        str(self.table1[ii].check_out_10), '%H:%M:%S').time()
                    xh, xm, xs = str(x).split(":")
                    yh, ym, ys = str(y).split(":")
                    in_time = timedelta(hours=float(
                        xh), minutes=float(xm), seconds=float(xs))
                    out_time = timedelta(hours=float(
                        yh), minutes=float(ym), seconds=float(ys))
                    diff = str(out_time - in_time)
                    if "day" in diff:
                        diff = diff.split("day, ")[1].split(":")
                        diff = timedelta(hours=float(diff[0]), minutes=float(
                            diff[1]), seconds=float(diff[2]))
                    else:
                        diff = out_time - in_time
                    total_time = total_time + diff

                if self.table1[ii].check_in_1:
                    shift_req = frappe.get_all("Shift Request", filters={'employee': self.employee,
                                                                        'from_date': ["<=", self.table1[ii].date], 'to_date': [">=", self.table1[ii].date]}, fields=["*"])
                    shift = None
                    if len(shift_req) > 0:
                        shift = shift_req[0].shift_type
                    else:
                        shift_ass = frappe.get_all("Shift Assignment", filters={'employee': self.employee,
                                                                                'date': ["<=", self.table1[ii].date]}, fields=["*"])
                        if len(shift_ass) > 0:
                            shift = shift_ass[0].shift_type
                    if shift == None:
                        frappe.throw(_("No shift available for this employee"))
                    self.table1[ii].shift = shift
                    shift_doc = frappe.get_doc("Shift Type", shift)
                    self.table1[ii].absent = 0
                    #hours_added = datetime.timedelta(hours = 2)
                    #next_value  = self.table1[ii].check_in_1 = hours_added
                    day_name = datetime.strptime(
                        str(self.table1[ii].date), '%Y-%m-%d').strftime('%A')

                    threshold = timedelta(hours=2, minutes=0, seconds=0)
                    in_diff = first_in_time - shift_doc.start_time
                   
                    day_data = None
                    # frappe.msgprint(str(day_name))
                    for day in shift_doc.days:
                        # frappe.msgprint(str(day.day))
                        if day_name == day.day:
                            day_data = day
                            break

                    if day_data.end_time > first_out_time:
                        per_day_h = first_out_time - first_in_time
                    else:
                        per_day_h = day_data.end_time - first_in_time
                    self.table1[ii].per_day_hour = per_day_h
                    total_per_day_h = total_per_day_h + per_day_h
                    # timedelta(hours=2, minutes=0, seconds=0)
                    req_working = day_data.end_time - day_data.start_time
                    if "day" in str(req_working):
                        req_working = str(req_working).split("day, ")[1].split(":")
                        # frappe.msgprint(str(req_working))
                        req_working = timedelta(hours=float(req_working[0]), minutes=float(
                            req_working[1]), seconds=float(req_working[2]))
                    if half_day_leave:
                        t = (flt(req_working.total_seconds())/3600)/2
                        required_working_hrs= required_working_hrs+t
                        #self.table1[ii].check_out_10 = t
                        

                    else:
                        required_working_hrs= required_working_hrs+round(
                                            flt(req_working.total_seconds())/3600, 2)
                    threshold = day_data.late_mark
                    half_day_time = day_data.half_day
                    late_mark = day_data.late_mark
                    in_diff = first_in_time - day_data.start_time
                    # frappe.msgprint(str(in_diff))
                    if "day" in str(in_diff):
                        in_diff = str(in_diff).split("day, ")[1].split(":")
                        # frappe.msgprint(str(in_diff))
                        in_diff = timedelta(hours=float(in_diff[0]), minutes=float(
                            in_diff[1]), seconds=float(in_diff[2]))

                    if first_in_time >= late_mark and first_in_time < half_day_time:
                        self.table1[ii].late = 1
                    if self.table1[ii].check_in_1 >= frappe.db.get_single_value('HR Settings', 'night_shift_start_time'):
                        self.no_of_nights += 1
                    else:
                        self.table1[ii].late = 0

                    if first_in_time >= half_day_time:
                        self.table1[ii].half_day = 1
                    else:
                        self.table1[ii].half_day = 0
                    if self.table1[ii].check_out_1:
                        out_diff = day_data.end_time - first_out_time
                        if "day" in str(out_diff):
                            out_diff = str(out_diff).split("day, ")[1].split(":")
                            out_diff = timedelta(hours=float(out_diff[0]), minutes=float(
                                out_diff[1]), seconds=float(out_diff[2]))

                        # frappe.msgprint(day_data.max_early)
                        # frappe.msgprint(str((out_diff.total_seconds()/60)))
                        # self.table1[ii].check_out_9 = out_diff.total_seconds()/60
                        # self.table1[ii].check_out_10 = day_data.max_early
                        if (out_diff.total_seconds()/60) > 15.00 and (out_diff.total_seconds()/60) <= float(day_data.max_early):

                            self.table1[ii].early = 1
                        elif (out_diff.total_seconds()/60) >= float(day_data.max_early) and (out_diff.total_seconds()/60) < float(day_data.max_half_day):

                            self.table1[ii].half_day = 1
                            self.table1[ii].early = 0
                        elif (out_diff.total_seconds()/60) > 720:
                            tmp  = (out_diff.total_seconds()/60) -720
                            if tmp > 15.00 and tmp <= float(day_data.max_early):

                                self.table1[ii].early = 1
                            elif tmp >= float(day_data.max_early) and tmp < float(day_data.max_half_day):

                                self.table1[ii].half_day = 1
                                self.table1[ii].early = 0 
                        elif (out_diff.total_seconds()/60) > float(day_data.max_half_day):
                            self.table1[ii].absent = 1
                            
                        else:
                            self.table1[ii].early = 0
                        if (out_diff.total_seconds()/60) > 720:
                            hrs = timedelta(hours=24, minutes=0,
                                            seconds=0) - out_diff
                            # if hrs > timedelta(hours=2, minutes=0,
                            #                 seconds=0):
                            self.table1[ii].late_sitting = hrs

                else:
                    self.table1[ii].absent = 1 
                    self.table1[ii].late = 0
                    self.table1[ii].half_day = 0
                    self.table1[ii].early = 0

                
                if self.table1[ii].absent==1 and half_day_leave:
                    if (total_time.total_seconds()/60) >= 255:
                        self.table1[ii].absent = 0
                        self.table1[ii].late = 0
                        self.table1[ii].half_day = 1
                        self.table1[ii].early = 0
                    
                    # frappe.msgprint(str(self.table1[ii].date))
                if self.table1[ii].early:
                    total_early += 1
                if self.table1[ii].late:
                    total_lates += 1
                if self.table1[ii].half_day:
                    total_half_days += 1
                if self.table1[ii].absent:
                    total_absents += 1

                total_hr_worked = total_hr_worked + total_time
                if self.table1[ii].late_sitting:
                    total_late_hr_worked = total_late_hr_worked + hrs
                self.table1[ii].difference = total_time  # time.strftime(
                #     "%H:%M:%S", time.gmtime(total_time))
                half_day_leave = False
            except:
                frappe.log_error(frappe.get_traceback(),"Attendance")
             

        self.hours_worked = round(
            flt((total_hr_worked-total_late_hr_worked).total_seconds())/3600, 2)
        self.late_sitting_hours = round(
            flt(total_late_hr_worked.total_seconds())/3600, 2)
        self.over_time = round(
            flt(total_late_hr_worked.total_seconds())/3600, 2)
        self.difference = round(
            (flt(self.hours_worked)-flt(required_working_hrs)), 2)
        self.total_absents = total_absents
        self.total_lates = total_lates
        self.total_early_goings = total_early
        self.total_half_days = total_half_days
        if self.difference > 0:
            #self.over_time = self.difference
            self.short_hours = 0
        else:
            #self.over_time = 0
            self.short_hours = self.difference

        self.total_working_hours = required_working_hrs