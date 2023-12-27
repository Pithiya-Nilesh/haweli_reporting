frappe.ready(function() {
    console.log(frappe.session.user);

    // Assuming you want to set the value in the 'user' field
    frappe.web_form.set_value('user', frappe.session.user);
});
