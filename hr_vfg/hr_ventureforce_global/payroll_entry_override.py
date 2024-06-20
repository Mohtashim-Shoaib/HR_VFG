import frappe
from frappe import _
from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe.model.document import Document
from frappe.utils import (
	DATE_FORMAT,
	add_days,
	add_to_date,
	cint,
	comma_and,
	date_diff,
	flt,
	getdate,
)
from hrms.hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
# from erpnext.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
from hr_vfg.hr_ventureforce_global.custom_events import create_salary_slips_for_employees

class CustomPayrollEntry(PayrollEntry):
    @frappe.whitelist()
    def create_salary_slips(self):
            """
            Creates salary slip for selected employees if already not created
            """
            self.check_permission("write")
            employees = [emp.employee for emp in self.employees]
            if employees:
                args = frappe._dict(
                    {
                        "salary_slip_based_on_timesheet": self.salary_slip_based_on_timesheet,
                        "payroll_frequency": self.payroll_frequency,
                        "start_date": self.start_date,
                        "end_date": self.end_date,
                        "company": self.company,
                        "posting_date": self.posting_date,
                        "deduct_tax_for_unclaimed_employee_benefits": self.deduct_tax_for_unclaimed_employee_benefits,
                        "deduct_tax_for_unsubmitted_tax_exemption_proof": self.deduct_tax_for_unsubmitted_tax_exemption_proof,
                        "payroll_entry": self.name,
                        "exchange_rate": self.exchange_rate,
                        "currency": self.currency,
                    }
                )
                if len(employees) > 30:
                    frappe.enqueue(create_salary_slips_for_employees, timeout=600, employees=employees, args=args)
                else:
                    create_salary_slips_for_employees(employees, args, publish_progress=False)
                    # since this method is called via frm.call this doc needs to be updated manually
                    self.reload()