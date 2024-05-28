// Copyright (c) 2024, Sanskar Technolab and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Working Report"] = {
	"filters": [
		{
            "fieldname": "employee",
            "label": "Employee Name",
            "fieldtype": "Link",
            "options": "User"
        },
        {
            "fieldname": "start_date",
            "label": "Start Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "end_date",
            "label": "End Date",
            "fieldtype": "Date"
        },

	]
};
