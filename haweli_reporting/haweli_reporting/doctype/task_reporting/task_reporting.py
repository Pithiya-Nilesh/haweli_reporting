# Copyright (c) 2023, Sanskar Technolab and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import throw, _
from frappe.utils import now
from frappe.utils.data import today
from frappe.utils import time_diff_in_hours


class TaskReporting(Document):
	def before_save(self):
		self.user = frappe.session.user
		self.reporting_time = now()
		self.reporting_date = today()
		self.working_hours = time_diff_in_hours(self.day_end_time, self.day_start_time)
		# self.first_name = frappe.get_value("User", filters={"name": frappe.session.user}, fieldname=["first_name"])
		# change_task_status(self)

	def validate(self):
		if self.day_start_time >= self.day_end_time:
			frappe.throw("start time is not after end time")

	def before_save(self):
		data = self.task_reporting_details
		for i in data:
			if i.is_completed:
				doc = frappe.get_doc("GP Task", i.task_details)
				doc.status = "Done"
				# doc.is_completed = 1
				doc.completed_by = frappe.session.user
				doc.save(ignore_permissions=True)
				frappe.db.commit()
			