# # Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# # License: GNU General Public License v3. See license.txt


# import datetime
# import math
# from operator import index

# import frappe
# from frappe import _, msgprint
# from frappe.model.naming import make_autoname
# from frappe.utils import (
# 	add_days,
# 	cint,
# 	cstr,
# 	date_diff,
# 	flt,
# 	formatdate,
# 	get_first_day,
# 	get_last_day,
# 	getdate,
# 	money_in_words,
# 	rounded,
# )
# import calendar
# from frappe.utils.background_jobs import enqueue
# from six import iteritems

# from erpnext.erpnext.setup.doctype.employee.employee import (
# 	InactiveEmployeeStatusError,
# 	get_holiday_list_for_employee,
# )

# # from erpnext.hr.doctype.employee.employee import (
# # 	InactiveEmployeeStatusError,
# # 	get_holiday_list_for_employee,
# # )

# import erpnext
# from erpnext.erpnext.accounts.utils import get_fiscal_year
# # from erpnext.accounts.utils import get_fiscal_year
# from hrms.hrms.hr.utils import get_holiday_dates_for_employee, validate_active_employee
# # from erpnext.hr.utils import get_holiday_dates_for_employee, validate_active_employee
# from erpnext.erpnext.loan_management.doctype.loan_repayment.loan_repayment import (
# 	calculate_amounts,
# 	create_repayment_entry,
# )

# # from erpnext.loan_management.doctype.loan_repayment.loan_repayment import (
# # 	calculate_amounts,
# # 	create_repayment_entry,
# # )
# from hrms.hrms.payroll.doctype.additional_salary.additional_salary import get_additional_salaries
# from hrms.hrms.payroll.doctype.employee_benefit_application.employee_benefit_application import(
# 	get_benefit_claim_amount
# )


# # from erpnext.payroll.doctype.additional_salary.additional_salary import get_additional_salaries
# # from erpnext.payroll.doctype.employee_benefit_application.employee_benefit_application import (
# # 	get_benefit_component_amount,
# # )
# from hrms.hrms.payroll.doctype.employee_benefit_claim.employee_benefit_claim import(
# 	get_benefit_claim_amount,
# 	get_last_payroll_period_benefits
# )
# # from erpnext.payroll.doctype.employee_benefit_claim.employee_benefit_claim import (
# # 	get_benefit_claim_amount,
# # 	get_last_payroll_period_benefits,
# # )
# from hrms.hrms.payroll.doctype.payroll_entry.payroll_entry import get_start_end_dates
# from hrms.hrms.payroll.doctype.payroll_period.payroll_period import (
# 	get_payroll_period,
# 	get_period_factor
# )
# # from erpnext.payroll.doctype.payroll_entry.payroll_entry import get_start_end_dates
# # from erpnext.payroll.doctype.payroll_period.payroll_period import (
# # 	get_payroll_period,
# # 	get_period_factor,
# # )
# # from erpnext.utilities.transaction_base import TransactionBase
# # from erpnext.payroll.doctype.salary_slip.salary_slip import SalarySlip
# from erpnext.erpnext.utilities.transaction_base import TransactionBase
# from hrms.hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip

# class CustomSalarySlip(SalarySlip):
# 	pass
# 	# def get_taxable_earnings_for_prev_period(self, payroll_period,start_date, end_date, allow_tax_exemption=False):
# 	# 	payroll_period = get_payroll_period(self.start_date, self.end_date, self.company)
# 	# 	prev = frappe.db.sql("""select previous_salary_earned from `tabPrevious Salary Detail` where employee=%s and payroll_period=%s""",
# 	# 		(self.employee,payroll_period.name))
		
# 	# 	prev_earned = flt(prev[0][0]) if prev else 0	
# 	# 	taxable_earnings = frappe.db.sql("""
# 	# 		select sum(sd.amount)
# 	# 		from
# 	# 			`tabSalary Detail` sd join `tabSalary Slip` ss on sd.parent=ss.name
# 	# 		where
# 	# 			sd.parentfield='earnings'
# 	# 			and sd.is_tax_applicable=1
# 	# 			and is_flexible_benefit=0
# 	# 			and ss.docstatus=1
# 	# 			and ss.employee=%(employee)s
# 	# 			and ss.start_date between %(from_date)s and %(to_date)s
# 	# 			and ss.end_date between %(from_date)s and %(to_date)s
# 	# 		""", {
# 	# 			"employee": self.employee,
# 	# 			"from_date": start_date,
# 	# 			"to_date": end_date
# 	# 		})
# 	# 	taxable_earnings = flt(taxable_earnings[0][0]) if taxable_earnings else 0

# 	# 	exempted_amount = 0
# 	# 	if allow_tax_exemption:
# 	# 		exempted_amount = frappe.db.sql("""
# 	# 			select sum(sd.amount)
# 	# 			from
# 	# 				`tabSalary Detail` sd join `tabSalary Slip` ss on sd.parent=ss.name
# 	# 			where
# 	# 				sd.parentfield='deductions'
# 	# 				and sd.exempted_from_income_tax=1
# 	# 				and is_flexible_benefit=0
# 	# 				and ss.docstatus=1
# 	# 				and ss.employee=%(employee)s
# 	# 				and ss.start_date between %(from_date)s and %(to_date)s
# 	# 				and ss.end_date between %(from_date)s and %(to_date)s
# 	# 			""", {
# 	# 				"employee": self.employee,
# 	# 				"from_date": start_date,
# 	# 				"to_date": end_date
# 	# 			})
# 	# 		exempted_amount = flt(exempted_amount[0][0]) if exempted_amount else 0

		
# 	# 	frappe.msgprint(str(prev_earned))
# 	# 	return (taxable_earnings + prev_earned) - exempted_amount
	
# 	# def get_tax_paid_in_period(self, start_date, end_date, tax_component):
# 	# 			payroll_period = get_payroll_period(self.start_date, self.end_date, self.company)
# 	# 			prev = frappe.db.sql("""select previous_tax_paid from `tabPrevious Salary Detail` where employee=%s and payroll_period=%s""",
# 	# 				(self.employee,payroll_period.name))
# 	# 			prev_paid = flt(prev[0][0]) if prev else 0
# 	# 			# find total_tax_paid, tax paid for benefit, additional_salary
# 	# 			total_tax_paid = flt(frappe.db.sql("""
# 	# 				select
# 	# 					sum(sd.amount)
# 	# 				from
# 	# 					`tabSalary Detail` sd join `tabSalary Slip` ss on sd.parent=ss.name
# 	# 				where
# 	# 					sd.parentfield='deductions'
# 	# 					and sd.salary_component=%(salary_component)s
# 	# 					and sd.variable_based_on_taxable_salary=1
# 	# 					and ss.docstatus=1
# 	# 					and ss.employee=%(employee)s
# 	# 					and ss.start_date between %(from_date)s and %(to_date)s
# 	# 					and ss.end_date between %(from_date)s and %(to_date)s
# 	# 			""", {
# 	# 				"salary_component": tax_component,
# 	# 				"employee": self.employee,
# 	# 				"from_date": start_date,
# 	# 				"to_date": end_date
# 	# 			})[0][0])

# 	# 			return total_tax_paid + prev_paid

# def add_leaves(doc, method):
# 		doc.annual_leave_ = frappe.db.get_value("Leave Application", 
# 					   {"from_date":[">=",doc.start_date],"to_date":["<=",doc.end_date],"status":"Approved","docstatus":1,
# 	                     "employee":doc.employee,"leave_type":"Annual Leave"},
# 					   "sum(total_leave_days)")
# 		doc.sick_leave = frappe.db.get_value("Leave Application", 
# 					   {"from_date":[">=",doc.start_date],"to_date":["<=",doc.end_date],"status":"Approved","docstatus":1,
# 	                     "employee":doc.employee,"leave_type":"Sick Leave"},
# 					   "sum(total_leave_days)")
# 		doc.emergency_leave = frappe.db.get_value("Leave Application", 
# 					   {"from_date":[">=",doc.start_date],"to_date":["<=",doc.end_date],"status":"Approved","docstatus":1,
# 	                     "employee":doc.employee,"leave_type":"Emergency Leave"},
# 					   "sum(total_leave_days)")
# 		doc.casual_leave = frappe.db.get_value("Leave Application", 
# 					   {"from_date":[">=",doc.start_date],"to_date":["<=",doc.end_date],"status":"Approved","docstatus":1,
# 	                     "employee":doc.employee,"leave_type":"Casual Leave"},
# 					   "sum(total_leave_days)")