// // Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// // For license information, please see license.txt
// /* eslint-disable */

// frappe.query_reports["Employee Individual Attendance"] = {
// 	"filters": [
// 		{
// 			fieldname:"depart",
// 			label: __("Department"),
// 			fieldtype: "Link",
// 			options: "Department",
// 			//default: 'Office Staff - F'
// 		},
// 		{
// 			"fieldname":"employee",
// 			"label": __("Employee"),
// 			"fieldtype": "Link",
// 			"options": "Employee",
// 			"reqd": 0,
		
// 				"get_query": function() {
// 					var dep = frappe.query_report.get_filter_value('depart');
// 					if(!dep){
// 						return {
// 							"doctype": "Employee",
// 							"filters": {
								
// 							}
// 						}
// 					}
// 					return {
// 						"doctype": "Employee",
// 						"filters": {
// 							"department": dep,
// 						}
// 					}
// 				}
// 		},
// 		{
// 			"fieldname":"month",
// 			"label": __("Month"),
// 			"fieldtype": "Select",
// 			"options":"\nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember",
// 			"reqd": 1
// 		},

// 	]
// };
