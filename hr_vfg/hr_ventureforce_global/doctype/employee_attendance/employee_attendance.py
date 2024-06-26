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
from datetime import date as dt
import datetime as special
import time
# from frappe.frappe.utils import cstr, flt, getdate, today, get_time
from frappe.utils import cstr, flt,getdate, today, get_time
import calendar


# from erpnext.setup.doctype.employee.employee import (
#     get_holidays_for_employee,
#     InactiveEmployeeStatusError
# )
from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee

# from erpnext.hr.doctype.employee.employee import (
# 	InactiveEmployeeStatusError,
# 	get_holiday_list_for_employee,
# )

# from erpnext.hr.doctype.employee.employee import (
# 	InactiveEmployeeStatusError,
# 	get_holiday_list_for_employee,
# )

class EmployeeAttendance(Document):
    # pass
    def autoname(self):
        self.name = make_autoname(self.employee + '-' + self.month)

    def validate(self):   
        total_early = 0
        total_lates = 0
        total_half_days = 0
        total_hr_worked = timedelta(hours=0, minutes=0, seconds=0)
        total_per_day_h = timedelta(hours=0, minutes=0, seconds=0)
        total_late_hr_worked = timedelta(hours=0, minutes=0, seconds=0)
        total_early_going_hrs= timedelta(hours=0, minutes=0, seconds=0)
        total_late_coming_hours = timedelta(hours=0, minutes=0, seconds=0)
        total_additional_hours = timedelta(hours=0, minutes=0, seconds=0)
        total_early_ot = timedelta(hours=0, minutes=0, seconds=0)
        total_approved_ot = timedelta(hours=0, minutes=0, seconds=0)
        required_working_hrs = 0.0
        holiday_halfday_ot =0
        holiday_full_day_ot =0
        self.no_of_holiday_night = 0
        self.total_absents = 0
        extra_ot_amount = 0
        holiday_doc = None
        self.total_public_holidays = 0
        half_day_leave = None
        self.no_of_nights = 0
        total_working_days=0
        present_days=0
        accun_holiday=0
        holidays = []
        hr_settings = frappe.get_single('V HR Settings')
        #try:
        month = self.get_month_no(self.month)
        year = int(self.year)
        _, num_days = calendar.monthrange(year, month)
        first_day = dt(year, month, 1)
        last_day = dt(year, month, num_days)
        if hr_settings.period_from != 1:
            if month == 1:
                temp_month = 12
            else:
                temp_month = month - 1
            first_day = dt(year, temp_month, int(hr_settings.period_from))
            last_day = dt(year, month, int(hr_settings.period_to))
            _, num_days = calendar.monthrange(year, temp_month)
            num_days = num_days - int(hr_settings.period_from) + int(hr_settings.period_to) + 1

        holidays = get_holidays_for_employee(self.employee,first_day,last_day)
        self.total_working_days = num_days -len(holidays)
        self.no_of_sundays = 0
        self.month_days = num_days
        # except:
        #     pass
        holiday_flag = False
        leave_flag = False
        total_holiday_hours = timedelta(hours=0,minutes=0,seconds=0)
        previous = None
        index = 0
        for data in self.table1:
            first_in_time = timedelta(hours=1,minutes=0,seconds=0)
            first_out_time = timedelta(hours=1,minutes=0,seconds=0)
            data.late_sitting = None
            data.additional_hours = None
            data.late_coming_hours = None
            data.early_going_hours = None
            data.early = 0
            data.total_ot_amount = 0
            tempdate = data.date
           
            if str(getdate(data.date)) in [str(d.holiday_date) for d in holidays]:
                        holiday_flag = True
                        data.public_holiday = 0
                        data.weekly_off = 0
                        for h in holidays:
                            if str(getdate(data.date)) == str(h.holiday_date):
                                if h.public_holiday == 1:
                                    data.public_holiday = 1
                                    self.total_public_holidays += 1
                                break
                        if data.public_holiday == 0: data.weekly_off = 1
                        if hr_settings.absent_sandwich in ['Absent Before Holiday']:
                            if previous and previous.absent == 1:
                                p_date = previous.date
                                lv = frappe.get_all("Leave Application", filters={"from_date":["<=",p_date],"to_date":[">=",p_date],"employee":self.employee,"status":"Approved"},fields=["*"])
                                if len(lv) > 0:
                                    pass
                                else:
                                    data.absent=1
                                    self.total_absents+=1
                                    continue
          
            
            if not holiday_flag:
                total_working_days+=1
            LA = frappe.get_all("Leave Application", filters={"from_date":["<=",tempdate],"to_date":[">=",tempdate],"employee":self.employee,"status":"Approved"},fields=["*"])
            if len(LA) > 0:
                leave_flag = True
                if LA[0].half_day:
                    half_day_leave = 1
                

           
            try:
                total_time = None
                hrs = timedelta(hours=0, minutes=0, seconds=0)
                s_type =None
                day_data = None
                # if not data.check_in_1 and data.check_out_1:
                #     data.check_in_1 = hr_settings.auto_fetch_check_in
                # if not data.check_out_1 and data.check_in_1:
                #     data.check_out_1 = hr_settings.auto_fetch_check_out

                if data.check_in_1 and data.check_out_1 and data.check_in_1 != data.check_out_1:
                    first_in_time = timedelta(hours=int(str(data.check_in_1).split(":")[0]),
                                              minutes=int(str(data.check_in_1).split(":")[1]))
                    first_out_time = timedelta(hours=int(str(data.check_out_1).split(":")[0]),
                                              minutes=int(str(data.check_out_1).split(":")[1]))
                   
                    diff = str(first_out_time - first_in_time)
                    if "day" in diff:
                        diff = diff.split("day, ")[1].split(":")
                        diff = timedelta(hours=float(diff[0]), minutes=float(
                            diff[1]), seconds=float(diff[2]))
                    else:
                        diff = first_out_time - first_in_time
                    total_time = total_time + diff if total_time else diff
                   
                if data.check_in_1 and data.check_in_1 != data.check_out_1:
                    shift = None
                    shift_ass = frappe.get_all("Shift Assignment", filters={'employee': self.employee,
                                                                            'start_date': ["<=", getdate(data.date)],'end_date': [">=", getdate(data.date)]}, fields=["*"])
                    if len(shift_ass) > 0:
                        shift = shift_ass[0].shift_type
                    else:
                        shift_ass = frappe.get_all("Shift Assignment", filters={'employee': self.employee,
                                                                            'start_date': ["<=", getdate(data.date)]}, fields=["*"])
                    if len(shift_ass) > 0:
                        shift = shift_ass[0].shift_type
                    if shift == None:
                        frappe.throw(_("No shift available for this employee"))
                    data.shift = shift
                    shift_doc = frappe.get_doc("Shift Type", shift)
                    s_type = shift_doc.shift_type
                    data.absent = 0
                   
                    day_name = datetime.strptime(
                        str(data.date), '%Y-%m-%d').strftime('%A')

                    in_diff = first_in_time - shift_doc.start_time
                   
                    day_data = None
                    for day in shift_doc.day:
                        if day_name == day.day:
                            day_data = day
                            break

                    if data.weekly_off == 1 or data.public_holiday == 1:
                        #settings required
                        if total_time:
                            total_holiday_hours += total_time
                            
                    if not day_data:
                        data.difference = total_time
                        check_sanwich_after_holiday(self,previous,data,hr_settings,index)
                        previous = data
                        index+=1
                        if data.absent == 0 and data.check_in_1:
                            if holiday_flag:
                                if hr_settings.count_working_on_holiday_in_present_days == 1:
                                    present_days+=1
                                if total_time:
                                    if total_time >= timedelta(hours=hr_settings.holiday_halfday_ot,minutes=00,seconds=0) and \
                                        total_time < timedelta(hours=hr_settings.holiday_full_day_ot,minutes=00,seconds=0):
                                        holiday_halfday_ot = holiday_halfday_ot + 1
                                    elif total_time >= timedelta(hours=hr_settings.holiday_full_day_ot,minutes=00,seconds=0):
                                        holiday_full_day_ot = holiday_full_day_ot + 1
                            else:
                                present_days+=1
                        continue
                    
                    if day_data.end_time > first_out_time:
                        per_day_h = first_out_time - first_in_time
                    else:
                        per_day_h = day_data.end_time - first_in_time
                    data.per_day_hour = per_day_h
                    if "day" in str(per_day_h):
                        per_day_h = str(per_day_h).split("day, ")[1].split(":")
                        per_day_h = timedelta(hours=float(per_day_h[0]), minutes=float(
                            per_day_h[1]), seconds=float(per_day_h[2]))
                    
                    data.per_day_hour = per_day_h
                    total_per_day_h = total_per_day_h + per_day_h
                    req_working = day_data.end_time - day_data.start_time
                    if "day" in str(req_working):
                        req_working = str(req_working).split("day, ")[1].split(":")
                        req_working = timedelta(hours=float(req_working[0]), minutes=float(
                            req_working[1]), seconds=float(req_working[2]))
                    if half_day_leave:
                        t = (flt(req_working.total_seconds())/3600)/2
                        required_working_hrs= required_working_hrs+t
                    else:
                        required_working_hrs= required_working_hrs+round(
                                            flt(req_working.total_seconds())/3600, 2)
                    half_day_time = day_data.half_day
                    late_mark = day_data.late_mark
                    in_diff = first_in_time - day_data.start_time
                    if not half_day_time:
                        half_day_time = day_data.late_mark
                    if "day" in str(in_diff):
                        in_diff = str(in_diff).split("day, ")[1].split(":")
                        in_diff = timedelta(hours=float(in_diff[0]), minutes=float(
                            in_diff[1]), seconds=float(in_diff[2]))

                    if first_in_time < day_data.start_time:
                        if first_in_time != timedelta(hours=0):
                            if day_data.early_overtime_start:
                                if first_in_time < day_data.early_overtime_start:
                                    first_in_time = day_data.early_overtime_start
                                data.early_overtime = day_data.start_time - first_in_time 
                                total_early_ot = total_early_ot + (day_data.start_time - first_in_time )
                            first_in_time = day_data.start_time

                    if first_in_time >= late_mark and first_in_time < half_day_time:
                        data.late = 1
                        if day_data.calculate_late_hours == "Late Mark":
                            data.late_coming_hours = first_in_time - late_mark
                        else:    
                            data.late_coming_hours = first_in_time - day_data.start_time
                    else:
                        data.late = 0
                    if shift_doc.shift_type == "Night":
                        if first_in_time > late_mark:
                            if (first_in_time - late_mark) > timedelta(hours=12,minutes=0,seconds=0):
                                data.late = 0
                            else:
                                data.late = 1
                        elif first_in_time < late_mark:
                            if (late_mark - first_in_time) > timedelta(hours=12,minutes=0,seconds=0):
                                data.late = 1
                            else:
                                data.late = 0

                                

                    if first_in_time >= frappe.db.get_single_value('V HR Settings', 'night_shift_start_time'):
                        self.no_of_nights += 1
                   

                    if first_in_time >= half_day_time and shift_doc.shift_type != "Night":
                        data.half_day = 1
                    else:
                        data.half_day = 0
                    
                    if shift_doc.shift_type == "Night":
                        if first_in_time > half_day_time:
                            if (first_in_time - half_day_time) > timedelta(hours=12,minutes=0,seconds=0):
                                data.half_day = 0
                            else:
                                data.late = 0
                                data.half_day = 1
                        elif first_in_time < half_day_time:
                            if (half_day_time - first_in_time) > timedelta(hours=12,minutes=0,seconds=0):
                                data.half_day = 1
                                data.late = 0
                            else:
                                data.half_day = 0
                    
                    if data.check_out_1:
                        out_diff = day_data.end_time - first_out_time
                        if "day" in str(out_diff):
                            out_diff = str(out_diff).split("day, ")[1].split(":")
                            out_diff = timedelta(hours=float(out_diff[0]), minutes=float(
                                out_diff[1]), seconds=float(out_diff[2]))

                        if (out_diff.total_seconds()/60) > 00.00 and (out_diff.total_seconds()/60) <= float(day_data.max_early):
                            if first_out_time < day_data.end_time:
                                data.early = 1
                        elif (out_diff.total_seconds()/60) >= float(day_data.max_early) and (out_diff.total_seconds()/60) < float(day_data.max_half_day):
                            data.half_day = 1
                            data.early = 0
                        elif (out_diff.total_seconds()/60) > 720:
                            tmp  = (out_diff.total_seconds()/60) -720
                            if tmp >= float(day_data.max_early) and tmp < float(day_data.max_half_day):
                                data.half_day = 1
                                data.early = 0 
                        elif (out_diff.total_seconds()/60) > float(day_data.max_half_day) and data.weekly_off==0 and data.public_holiday == 0:
                            if first_out_time < day_data.end_time:
                                data.absent = 1
                        else:
                            data.early = 0
                       
                        out_diff = day_data.over_time_start - first_out_time
                        
                        if "day" in str(out_diff):
                            out_diff = str(out_diff).split("day, ")[1].split(":")
                            out_diff = timedelta(hours=float(out_diff[0]), minutes=float(
                                out_diff[1]), seconds=float(out_diff[2]))
                        
                        ot_start  = day_data.over_time_start if day_data.over_time_start else day_data.end_time
                        if (out_diff.total_seconds()/60) > 720 and first_out_time < ot_start and shift_doc.shift_type!="Night":
                            hrs = timedelta(hours=24, minutes=0,
                                            seconds=0) - out_diff
                            hrs = hrs
                            data.late_sitting = hrs
                        if (out_diff.total_seconds()/60) > 720 and first_out_time > ot_start and shift_doc.shift_type!="Night":
                            hrs = timedelta(hours=24, minutes=0,
                                            seconds=0) - out_diff
                           
                            hrs = hrs
                            data.late_sitting = hrs
                        if first_out_time > ot_start and shift_doc.shift_type == "Night":
                            hrs = timedelta(hours=24, minutes=0,
                                            seconds=0) - out_diff
                            hrs = hrs
                            data.late_sitting = hrs
                        if data.absent == 1 or not data.check_out_1:
                            data.late_sitting = None
                        #setting required
                        if data.late_sitting:
                            if data.late_sitting >= timedelta(hours=hr_settings.double_overtime_after,minutes=0,seconds=0):
                                data.late_sitting = data.late_sitting + data.late_sitting
                            if data.late_sitting > timedelta(hours=hr_settings.threshold_for_additional_hours,minutes=0,seconds=0):
                                    data.additional_hours  =  data.late_sitting - timedelta(hours=hr_settings.threshold_for_additional_hours,minutes=0,seconds=0)
                                    total_additional_hours = total_additional_hours + data.additional_hours

                        if first_out_time >= timedelta(hours=get_time(hr_settings.night_shift_start_time).hour,minutes=get_time(hr_settings.night_shift_start_time).minute) and holiday_flag:
                            data.holiday_night = 1
                            self.no_of_holiday_night+=1

                else:
                    if data.weekly_off==0 and data.public_holiday == 0:
                        data.absent = 1 
                        data.late = 0
                        data.half_day = 0
                        data.early = 0

                if total_time:
                    total_time_hours = total_time.total_seconds()/3600
                    if total_time_hours >= day_data.minimum_hours_for_present:
                        if day_data.minimum_hours_for_present > 0:
                            data.absent = 0
                            data.half_day = 0
                    elif total_time_hours >= day_data.minimum_hours_for_half_day:
                        if day_data.minimum_hours_for_half_day > 0:
                            data.half_day = 1
                    else:
                        if (day_data.minimum_hours_for_half_day > 0 and day_data.minimum_hours_for_present > 0) \
                             or total_time_hours < day_data.minimum_hours_for_absent :
                            data.absent = 1
                            data.half_day = 0
                            data.early = 0
                            data.late = 0
                if hr_settings.late_and_early_mark:
                    if data.early==1 and data.late == 1:
                        data.half_day = 1
                elif hr_settings.late_mark:
                    if data.late == 1:
                        data.half_day = 1
                elif hr_settings.early_mark:
                    if data.early==1:
                        data.half_day = 1
                if day_data:
                    if day_data.end_time > first_out_time and data.early ==1:
                        data.early_going_hours =  day_data.end_time - first_out_time
                        if day_data.calculate_early_hours == "Exit Grace Period":
                                    data.early_going_hours = data.early_going_hours - timedelta(hours=0,minutes=int(day_data.max_early),seconds=0)
                        #total_early_going_hrs = total_early_going_hrs + data.early_going_hours
                if data.weekly_off==1 or data.public_holiday == 1:
                     data.absent = 0 
                
                if first_in_time:
                    if first_in_time >= timedelta(hours=get_time(hr_settings.night_shift_start_time).hour,minutes=get_time(hr_settings.night_shift_start_time).minute) or s_type == "Night":
                        data.night = 1
                
               
                if data.early:
                    total_early += 1
                if data.late:
                    total_lates += 1
                    # if data.late_coming_hours:
                    #     total_late_coming_hours = total_late_coming_hours + data.late_coming_hours
                if data.half_day:
                    total_half_days += 1
              
                if data.absent == 1:
                    self.total_absents +=1
                if data.half_day == 1:
                    if data.absent == 1:
                        data.absent = 0
                        self.total_absents -=1
                if data.absent == 0 and data.check_in_1:
                    if holiday_flag:
                        if hr_settings.count_working_on_holiday_in_present_days == 1:
                            present_days+=1
                    else:
                     present_days+=1
                

                if total_time:    
                    total_hr_worked = total_hr_worked + total_time
                
                if data.late_sitting and data.weekly_off == 0 and data.public_holiday == 0:
                    total_late_hr_worked = total_late_hr_worked + data.late_sitting
                    if day_data.overtime_slabs:
                        OT_slabs = frappe.get_doc("Overtime Slab",day_data.overtime_slabs)
                        late_hours = round(
                                    flt((data.late_sitting).total_seconds())/3600, 2)
                       
                        amount = 0
                        for sl in OT_slabs.slabs:
                            if flt(late_hours) <= flt(sl.hours):
                               amount  = sl.amount
                            if flt(sl.hours) > flt(late_hours):
                                break
                            #for case if late sitting hours are greater than all slabs
                            amount  = sl.amount
                            
                        data.total_ot_amount = amount
                        extra_ot_amount+=amount

                

                data.difference = total_time  
                if holiday_flag == True and getdate(tempdate) <= getdate(today()):
                    accun_holiday+=1
                if data.extra_absent:
                    self.total_absents+=1
               
                if holiday_flag:
                     self.no_of_sundays+=1
                     if total_time:
                                    if total_time >= timedelta(hours=hr_settings.holiday_halfday_ot,minutes=00,seconds=0) and \
                                        total_time < timedelta(hours=hr_settings.holiday_full_day_ot,minutes=00,seconds=0):
                                        holiday_halfday_ot = holiday_halfday_ot + 1
                                    elif total_time >= timedelta(hours=hr_settings.holiday_full_day_ot,minutes=00,seconds=0):
                                        holiday_full_day_ot = holiday_full_day_ot + 1
                half_day_leave = False
                holiday_flag = False
                if day_data:
                    if day_data.late_slab and data.late_coming_hours:
                        lsm = frappe.db.get_value("Late Slab",{"name":day_data.late_slab},"late_slab_minutes")
                        if data.late_coming_hours > timedelta(hours=0,minutes=int(lsm)):
                            data.late_coming_hours = data.late_coming_hours - timedelta(hours=0,minutes=int(lsm))
                            total_late_coming_hours = total_late_coming_hours + data.late_coming_hours
                    if day_data.early_slab and data.early_going_hours:
                        esm = frappe.db.get_value("Early Slab",{"name":day_data.early_slab},"early_slab_minutes")
                        if data.early_going_hours > timedelta(hours=0,minutes=int(esm)):
                            data.early_going_hours = data.early_going_hours - timedelta(hours=0,minutes=int(esm))
                            total_early_going_hrs = total_early_going_hrs + data.early_going_hours
                    
                if data.approved_ot1:
                    total_approved_ot+= timedelta(hours=int(str(data.approved_ot1).split(":")[0]),minutes=int(str(data.approved_ot1).split(":")[1]))
                check_sanwich_after_holiday(self,previous,data,hr_settings,index)
               
                previous = data
                index+=1
               
            except:
                frappe.log_error(frappe.get_traceback(),"Attendance")
                previous = data
             

        self.hours_worked = round(
            flt((total_hr_worked-total_late_hr_worked).total_seconds())/3600, 2)
        self.late_sitting_hours = round(
            flt(total_late_hr_worked.total_seconds())/3600, 2)
        self.holiday_halfday_ot = holiday_halfday_ot
        self.holiday_full_day_ot = holiday_full_day_ot
        self.over_time = self.late_sitting_hours
        # self.difference = round(
        #     (flt(self.hours_worked)-flt(required_working_hrs)), 2)
        if self.over_time >= 1:
            self.over_time = round(self.over_time)
        else:
            self.over_time = 0.0
        self.difference = round(
            flt(total_late_coming_hours.total_seconds())/3600, 2)
        self.approved_ot = round(
            flt(total_approved_ot.total_seconds())/3600, 2)
        
        self.extra_hours = round(
            flt(total_additional_hours.total_seconds())/3600, 2)
        self.extra_ot_amount = extra_ot_amount
        self.total_lates = total_lates
        self.total_early_goings = total_early
        self.total_half_days = total_half_days
        self.total_early_going_hours = total_early_going_hrs
        self.holiday_hour = round(flt(total_holiday_hours.total_seconds())/3600, 2)
        self.early_over_time = round(flt(total_early_ot.total_seconds())/3600, 2)
        t_lat = 0
        t_earl = 0
        if hr_settings.maximum_lates_for_absent > 0:
            t_lat = int(total_lates/hr_settings.maximum_lates_for_absent) if total_lates >= hr_settings.maximum_lates_for_absent else 0
        self.lates_for_absent = t_lat

        if hr_settings.maximum_early_for_absent > 0:
            t_earl = int(total_early/hr_settings.maximum_early_for_absent) if total_early >= hr_settings.maximum_early_for_absent else 0
        self.early_for_absents = t_earl
       
        self.short_hours = self.difference
       
        self.total_working_hours = round(required_working_hrs,2)
        self.total_difference_hours = round(self.total_working_hours - self.hours_worked,2)
        self.late_plus_early_hours_ = total_late_coming_hours + self.total_early_going_hours
        self.present_days = present_days 
        lfh = 0
        if hr_settings.maximum_lates_for_halfday > 0:
            lfh = int(total_lates/hr_settings.maximum_lates_for_halfday) if total_lates >= hr_settings.maximum_lates_for_halfday else 0
        self.lates_for_halfday = round(lfh/2,1)

        efh = 0
        if hr_settings.maximum_early_for_halfday > 0:
            efh = int(total_early/hr_settings.maximum_early_for_halfday) if total_early >= hr_settings.maximum_early_for_halfday else 0
        self.early_for_halfday = round(efh/2,1)

    def get_month_no(self, month):
        dict_={
            "January":1,
            "February":2,
            "March":3,
            "April":4,
            "May":5,
            "June":6,
            "July":7,
            "August":8,
            "September":9,
            "October":10,
            "November":11,
            "December":12
        }
        return dict_[month]
    

def check_sanwich_after_holiday(self, previous,data,hr_settings,index):
    ab_index = []
    ab_index_process = False
    if data.absent == 1:
        for num in reversed(range(index)) :
            if self.table1[num].weekly_off ==1 or self.table1[num].public_holiday==1:
                ab_index.append(num)
            else:
                if hr_settings.absent_sandwich == 'Absent After Holiday':
                    ab_index_process = True
                    break
                elif hr_settings.absent_sandwich == 'Absent Before and After Holiday' and self.table1[num].absent == 1:
                        ab_index_process = True
                        break
            
    if ab_index_process:
        for ind in ab_index:
                if self.table1[ind].absent != 1:
                    self.table1[ind].absent = 1
                    self.no_of_sundays-=1
                    if self.table1[ind].difference:
                        if self.table1[ind].difference >= timedelta(hours=hr_settings.holiday_halfday_ot,minutes=00,seconds=0) and \
                            self.table1[ind].difference < timedelta(hours=hr_settings.holiday_full_day_ot,minutes=00,seconds=0):
                           self.holiday_halfday_ot = self.holiday_halfday_ot - 1
                        elif self.table1[ind].difference >= timedelta(hours=hr_settings.holiday_full_day_ot,minutes=00,seconds=0):
                            self.holiday_full_day_ot = self.holiday_full_day_ot - 1
                    self.total_absents += 1



def get_holidays_for_employee(
	employee, start_date, end_date, raise_exception=True, only_non_weekly=False
):
	"""Get Holidays for a given employee

	`employee` (str)
	`start_date` (str or datetime)
	`end_date` (str or datetime)
	`raise_exception` (bool)
	`only_non_weekly` (bool)

	return: list of dicts with `holiday_date` and `description`
	"""
	holiday_list = get_holiday_list_for_employee(employee, raise_exception=raise_exception)

	if not holiday_list:
		return []

	filters = {"parent": holiday_list, "holiday_date": ("between", [start_date, end_date])}

	if only_non_weekly:
		filters["weekly_off"] = False

	holidays = frappe.get_all("Holiday", fields=["description","public_holiday", "holiday_date"], filters=filters)

	return holidays