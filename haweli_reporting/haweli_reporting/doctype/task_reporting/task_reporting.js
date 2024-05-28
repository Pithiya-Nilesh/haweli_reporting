// Copyright (c) 2023, Sanskar Technolab and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Task Reporting", {
//     day_start_time(frm){
//         if (frm.doc.day_start_time >= frm.doc.day_end_time){
//             frappe.throw("start time is not set after end time")
//         }

//         if (frm.doc.day_start_time && frm.doc.day_end_time) {
//             frm.doc.working_hours = calculateWorkingHours(frm.doc.day_start_time, frm.doc.day_end_time);
//             frm.refresh_field('working_hours');
//         }
//     },
//     day_end_time(frm){
//         if (frm.doc.day_start_time >= frm.doc.day_end_time){
//             frappe.throw("end time is not set before start time")
//         }

//         if (frm.doc.day_start_time && frm.doc.day_end_time) {
//             frm.doc.working_hours = calculateWorkingHours(frm.doc.day_start_time, frm.doc.day_end_time);
//             frm.refresh_field('working_hours');
//         }
//     }
// });

// function calculateWorkingHours(start_time, end_time) {
//     var start = moment(start_time, 'HH:mm:ss');
//     var end = moment(end_time, 'HH:mm:ss');

//     // Calculate the difference in hours and minutes
//     var duration = moment.duration(end.diff(start));

//     // Convert the difference to hours and round to two decimal places
//     var hours = duration.asHours().toFixed(2);

//     return hours;
// }



// cur_frm.cscript.onload = function(frm) {     		
//     cur_frm.set_query("task_details", "task_reporting_details", function() {
//         return {
//             filters: [
//                 ["assigned_to", "=", frappe.session.user],
//                 ["status", "!=", "Done"]
//             ]
//         };
//     });
// }


// frappe.ui.form.on('Task Reporting Details', {
// 	start_time: function(frm, cdt, cdn) {
//         var data = locals[cdt][cdn]
//         var start_time = data.start_time
//         var day_start_time = frm.doc.day_start_time

//         if (day_start_time >= start_time) {
//             frappe.model.set_value(cdt, cdn, 'start_time', '');
//             frm.refresh()
//             frappe.throw(__("Task start time must be after the day start time."));
//         }

//         if (start_time < data.end_time){
//             frappe.throw("end time is not set before start time")
//         }

// 	},

//     end_time: function(frm, cdt, cdn) {
//         var data = locals[cdt][cdn]
//         var end_time = data.end_time
//         var day_end_time = frm.doc.day_end_times

//         if (end_time >= day_end_time) {
//             frappe.model.set_value(cdt, cdn, 'end_time', '');
//             frm.refresh()
//             frappe.throw(__("Task end time must be before the day end time."));
//         }

//         if (end_time < data.start_time){
//             frappe.throw("end time is not set before start time")
//         }
// 	}
// });


frappe.ui.form.on('Timing Report', {
    refresh(frm) {
       
    },
    time: function(frm, cdt, cdn) {
        calculate_working_hours(frm, cdt, cdn);
    },
    end_time: function(frm, cdt, cdn) {
        calculate_working_hours(frm, cdt, cdn);
    }
});


function calculate_working_hours(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.time && row.end_time) {
        // Convert times to moment objects
        let start_time = moment(row.time, 'HH:mm:ss');
        let end_time = moment(row.end_time, 'HH:mm:ss');

        // Calculate duration in hours
        let duration = moment.duration(end_time.diff(start_time));
        let hours = duration.asHours();
        
        frappe.model.set_value(cdt, cdn, 'working_hours', hours);
    }
}
