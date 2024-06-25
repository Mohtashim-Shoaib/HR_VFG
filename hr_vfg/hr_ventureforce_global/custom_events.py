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
# from erpnext.payroll.doctype.payroll_entry.payroll_entry import get_existing_salary_slips
from hrms.payroll.doctype.payroll_entry.payroll_entry import get_existing_salary_slips

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
				
def create_salary_slips_for_employees(employees, args, publish_progress=True):
        salary_slips_exists_for = get_existing_salary_slips(employees, args)
        count = 0
        salary_slips_not_created = []
        for emp in employees:
            if emp not in salary_slips_exists_for:
                e_month  = getdate(args.get("end_date")).month
                year = getdate(args.get("end_date")).year
                month_str  = ["January", "February", "March", "April","May","June","July","August","September","October","November","December"][e_month-1]
                try:
                    employee_att = frappe.get_all("Employee Attendance",
                    filters={"month":month_str,"employee": emp,"year":year},fields=["*"])[0]
                    
                    args.update({
                    "select_month": month_str,
                    "employee_attendance": employee_att.name,
                    # "lates": employee_att.total_lates,
                    # "early_goings": employee_att.early_goings,
                    # "late_sitting_hours": employee_att.late_sitting_hours,
                    # "present_day": employee_att.present_days,
                    # "over_times": employee_att.over_time,
                    # "short_hours": employee_att.short_hours,
                    # "absents": employee_att.total_absents,
                    # "half_days": employee_att.total_half_days,
                    # "late_adjusted_absents":int(employee_att.total_lates)/3,
                    
                    })

                except:
                    frappe.error_log(frappe.get_traceback(),"PAYROLL")
                args.update({"doctype": "Salary Slip", "employee": emp})
                ss = frappe.get_doc(args)
                ss.insert()
                count += 1
                if publish_progress:
                    frappe.publish_progress(
                        count * 100 / len(set(employees) - set(salary_slips_exists_for)),
                        title=_("Creating Salary Slips..."),
                    )

            else:
                salary_slips_not_created.append(emp)

        payroll_entry = frappe.get_doc("Payroll Entry", args.payroll_entry)
        payroll_entry.db_set("salary_slips_created", 1)
        payroll_entry.notify_update()

        if salary_slips_not_created:
            frappe.msgprint(
                _(
                    "Salary Slips already exists for employees {}, and will not be processed by this payroll."
                ).format(frappe.bold(", ".join([emp for emp in salary_slips_not_created]))),
                title=_("Message"),
                indicator="orange",
            )
