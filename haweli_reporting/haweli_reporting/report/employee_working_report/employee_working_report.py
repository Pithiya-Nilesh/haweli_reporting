import frappe

def execute(filters=None):
    columns, data = [], []

    
    columns = [
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 250,
        },
        {
            "label": "Date",
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 150,
        },
      
        {
            "label": "Working Hours",
            "fieldname": "working_hours",
            "fieldtype": "Float",
            "width": 150,
        },
        
    ]
    
   
    logged_in_user = frappe.session.user
    
    is_admin_or_specific_user = (
        "Administrator" in frappe.get_roles(logged_in_user) or 
        logged_in_user == "anand@gmail.com"
    )
    
    
    if not is_admin_or_specific_user:
        permitted_users = [d.for_value for d in frappe.get_all("User Permission", filters={"user": logged_in_user}, fields=["for_value"])]
       
        if logged_in_user not in permitted_users:
            permitted_users.append(logged_in_user)
    else:
        permitted_users = []

   
    sql = """
        SELECT 
            tr.first_name AS employee_name,
            tr.user AS user,
            ti.date AS date,
            ti.time AS start_time,
            ti.end_time AS end_time,
            SUM(ti.working_hours) AS working_hours,
            ti.description AS description
        FROM 
            `tabTask Reporting` tr
        JOIN 
            `tabTiming Report` ti ON ti.parent = tr.name
    """
    
    conditions = []
    sql_args = []

    if not is_admin_or_specific_user:
        sql += " WHERE tr.user IN ({})".format(", ".join(["%s"] * len(permitted_users)))
        sql_args.extend(permitted_users)

   
    if filters.get("start_date"):
        conditions.append("ti.date >= %s")
        sql_args.append(filters.get("start_date"))
    if filters.get("end_date"):
        conditions.append("ti.date <= %s")
        sql_args.append(filters.get("end_date"))
    if filters.get("employee"):
        conditions.append("tr.user = %s")
        sql_args.append(filters.get("employee"))
    
    if conditions:
        if not is_admin_or_specific_user:
            sql += " AND " + " AND ".join(conditions)
        else:
            sql += " WHERE " + " AND ".join(conditions)
        
    sql += " GROUP BY tr.first_name, ti.date"

    data = frappe.db.sql(sql, tuple(sql_args), as_dict=True)

    return columns, data
