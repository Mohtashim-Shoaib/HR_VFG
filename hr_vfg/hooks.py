from . import __version__ as app_version

app_name = "hr_vfg"
app_title = "HR VentureForce Global"
app_publisher = "VFG"
app_description = "HR VentureForce Global"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "shahrukh@telniasoft.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/hr_vfg/css/hr_vfg.css"
# app_include_js = "/assets/hr_vfg/js/hr_vfg.js"

# include js, css files in header of web template
# web_include_css = "/assets/hr_vfg/css/hr_vfg.css"
# web_include_js = "/assets/hr_vfg/js/hr_vfg.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "hr_vfg/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "hr_vfg.install.before_install"
# after_install = "hr_vfg.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "hr_vfg.uninstall.before_uninstall"
# after_uninstall = "hr_vfg.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "hr_vfg.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Payroll Entry": "hr_vfg.hr_ventureforce_global.payroll_entry_override.CustomPayrollEntry",
    "Salary Slip":"hr_vfg.hr_ventureforce_global.salary_slip_override.CustomSalarySlip"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"Salary Slip": {
# 		"validate": "hr_vfg.hr_ventureforce_global.salary_slip_override.add_leaves",
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"hr_vfg.tasks.all"
#	],
#	"daily": [
#		"hr_vfg.tasks.daily"
#	],
#	"hourly": [
#		"hr_vfg.tasks.hourly"
#	],
#	"weekly": [
#		"hr_vfg.tasks.weekly"
#	]
#	"monthly": [
#		"hr_vfg.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "hr_vfg.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"erpnext.payroll.doctype.payroll_entry.payroll_entry.create_salary_slips": "hr_vfg.hr_ventureforce_global.custom_events.create_salary_slips"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "hr_vfg.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"hr_vfg.auth.validate"
# ]

