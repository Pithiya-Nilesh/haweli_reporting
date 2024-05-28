import frappe

def execute(filters=None):
    columns, data = [], []

    # Define the columns for the report
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
        # {
        #     "label": "Start Time",
        #     "fieldname": "start_time",
        #     "fieldtype": "Time",
        #     "width": 150,
        # },
        # {
        #     "label": "End Time",
        #     "fieldname": "end_time",
        #     "fieldtype": "Time",
        #     "width": 150,
        # },
        {
            "label": "Working Hours",
            "fieldname": "working_hours",
            "fieldtype": "Float",
            "width": 150,
        },
        # {
        #     "label": "Description",
        #     "fieldname": "description",
        #     "fieldtype": "Small Text",
        #     "width": 150,
        # },
    ]
    
    # Base SQL query
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
        WHERE 1=1
    """
    
  
    conditions = []

    
    if filters.get("start_date"):
        conditions.append("ti.date >= %s")
    if filters.get("end_date"):
        conditions.append("ti.date <= %s")
    if filters.get("employee"):
        conditions.append("tr.user = %s")  

    
    if conditions:
        sql += " AND " + " AND ".join(conditions)
        
    sql += " GROUP BY tr.first_name, ti.date"    

    sql_args = []
    if filters.get("start_date"):
        sql_args.append(filters.get("start_date"))
    if filters.get("end_date"):
        sql_args.append(filters.get("end_date"))
    if filters.get("employee"):
        sql_args.append(filters.get("employee"))

    data = frappe.db.sql(sql, tuple(sql_args), as_dict=True)
    print(data)

    return columns, data
