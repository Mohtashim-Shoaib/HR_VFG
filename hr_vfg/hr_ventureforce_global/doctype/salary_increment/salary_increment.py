# -*- coding: utf-8 -*-
# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# from __future__ import unicode_literals
# import frappe
# from frappe.model.document import Document

# class SalaryIncrement(Document):
	# pass
	# def validate(self):
	# 	# if len(self.salary_increment_table) == 0:
	# 	# 	incs = frappe.get_all("Salary Increment",filters={"employee":self.employee,"name":["!=",self.name]},fields=["*"])
	# 	# 	for doc in incs:
	# 	# 		self.append("salary_increment_table",{
	# 	# 			"increment_date":doc.increment_date,
	# 	# 			"increment_type":doc.increment_type,
	# 	# 			"previous_salary":doc.salary,
	# 	# 			"increment_per":doc.increment_percentage,
	# 	# 			"increment_amount":doc.increment_amount,
	# 	# 			"after_increment_salary":doc.after_increment_salary
	# 	# 		})
	# 	for d in self.salary_increment_table:
	# 		for inn_d in self.salary_increment_table:
	# 			if d.employee == inn_d.employee and d.name != inn_d.name:
	# 				frappe.throw("Employee {0} selected multiple times".format(d.employee))
	# @frappe.whitelist()
	# def get_employee(self,employee=None,department=None,designation=None,branch=None):
	# 	self.salary_increment_table = []
	# 	filters = {"status":"Active"}
	# 	if employee:
	# 		filters["name"] = employee
	# 	else:
	# 		if department:
	# 			filters["department"] = department
	# 		if designation:
	# 			filters["designation"] = designation
	# 		if branch:
	# 			filters["branch"] = branch
	# 	employees = frappe.db.get_all("Employee",filters=filters,fields=["name"])
	# 	for row in employees:
	# 		prev = frappe.db.get_value("Salary Structure Assignment",{"docstatus":1,"employee":row.name},"base") or 0
	# 		self.append("salary_increment_table",{
	# 			    "employee":row.name,
	# 				"increment_date":self.increment_date,
	# 				"increment_type":self.increment_type,
	# 				"previous_salary":prev,
	# 				"increment_per":self.increment_percentage,
	# 				"increment_amount":prev*(self.increment_percentage/100),
	# 				"after_increment_salary":prev + (prev*(self.increment_percentage/100))
	# 			})
	# 	self.save()
	# def on_submit(self):
	# 	for d in self.salary_increment_table:
	# 		emp_doc = frappe.get_doc("Employee",d.employee)
	# 		emp_doc.update({
	# 			"salary":d.after_increment_salary
	# 		})
	# 		emp_doc.save()
	# 		ssa_value = frappe.db.get_value("Salary Structure Assignment",{"employee":d.employee,"docstatus":1},"name")
	# 		if ssa_value:
	# 			ssa_doc = frappe.get_doc("Salary Structure Assignment",ssa_value)
	# 			new_doc = frappe.copy_doc(ssa_doc)
	# 			new_doc.update({
	# 				"from_date":self.increment_date,
	# 				"base":self.after_increment_salary
	# 			})
	# 			new_doc.save()
	# 			new_doc.submit()

