# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals, absolute_import
from frappe.model.document import Document
from six.moves import range
from six import string_types
import frappe
import json
from email.utils import formataddr
from frappe.utils import (get_url, get_formatted_email, cint,
	validate_email_add, split_emails, time_diff_in_seconds, parse_addr)
from frappe.utils.file_manager import get_file
from frappe.email.queue import check_email_limit
from frappe.utils.scheduler import log
from frappe.email.email_body import get_message_id
import frappe.email.smtp
import time
from frappe import _
from frappe.utils.background_jobs import enqueue

class AttendanceEmail(Document):
	pass

@frappe.whitelist()
def send_email_now(name, diff, date, emp_name, month, total_working_hours, hours_worked, difference, email_id,aaj, ci1, ci2, ci3, ci4, ci5, ci6, ci7, ci8, ci9, ci10, co1, co2, co3, co4, co5, co6, co7, co8, co9, co10, ):
	frappe.sendmail(recipients=email_id,
		subject="Attendance Report of "+aaj,
		message= """Dear """+emp_name+""", Your attendance report of """+aaj+""",<br><br>

<table style='border-left: 1px solid #000;font-size:11px;border-top: 1px solid #000;' width='80%' cellspacing='0' cellpadding='10' align='center'>
<tbody>
<tr>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Date</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Total Hours</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check In</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check Out</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check In</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check Out</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check In</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check Out</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check In</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check Out</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check In</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check Out</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check In</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check Out</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check In</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check Out</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check In</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check Out</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check In</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check Out</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check In</th>
<th style='border-right:1px solid #000;border-bottom:1px solid #000;background-color:#B4C6E7; text-align: center;'>Check Out</th>
</tr>

<tr>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+date+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+diff+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+ci1+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+co1+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+ci2+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+co2+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+ci3+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+co3+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+ci4+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+co4+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+ci5+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+co5+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+ci6+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+co6+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+ci7+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+co7+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+ci8+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+co8+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+ci9+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+co9+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+ci10+"""</td>
<td style='border-right:1px solid #000;border-bottom:1px solid #000; text-align: center;'>"""+co10+"""</td>
</tr>
</tbody>
</table>
<br><br>


Total Working hours for the whole month till now : """+total_working_hours+""",<br>
Total hours to be worked for the whole month till now : """+hours_worked+""",<br>
Total Difference hours for the whole month till now : """+difference)