# admin_interface.py

import streamlit as st
import psycopg2

def render_admin_interface(cursor, conn):
    menu = st.sidebar.selectbox('Select an Operation', ('View Employees', 'Add Employee', 'View Departments', 'Add Department', 'View Salary', 'Add Salary', 'View Attendance', 'Add Attendance', 'Update Employee', 'Delete Employee'))

    if menu == "View Employees":
        st.subheader("View Employees")
        cursor.execute("SELECT * FROM Employees")
        employees = cursor.fetchall()
        for employee in employees:
            st.write("EmployeeID:", employee[0])
            st.write("Name:", employee[1])
            st.write("Email:", employee[2])
            st.write("Department:", employee[3])
            st.write("Job Title:", employee[4])
            st.write("-----------------------------------")

    # elif menu == "Add Employee":
    #     st.subheader("Add Employee")
    #     employee_id = st.number_input("Employee ID")
    #     name = st.text_input("Name")
    #     email = st.text_input("Email")
    #     department = st.text_input("Department")
    #     job_title = st.text_input("Job Title")
    #     if st.button("Add"):
    #         cursor.execute("INSERT INTO Employees (EmployeeID, Name, Email, Department, JobTitle) VALUES (%s, %s, %s, %s, %s)", (employee_id, name, email, department, job_title))
    #         conn.commit()
    #         st.success("Employee added successfully")
    elif menu == "Add Employee":
        st.subheader("Add Employee")
        employee_id = st.number_input("Employee ID")
        name = st.text_input("Name")
        email = st.text_input("Email")
        department_options = get_department_options(cursor)
        department = st.selectbox("Department", department_options)
        job_title = st.text_input("Job Title")
        if st.button("Add"):
            cursor.execute("INSERT INTO Employees (EmployeeID, Name, Email, Department, JobTitle) VALUES (%s, %s, %s, %s, %s)", (employee_id, name, email, department, job_title))
            conn.commit()
            st.success("Employee added successfully")

    elif menu == "View Departments":
        st.subheader("View Departments")
        cursor.execute("SELECT * FROM Departments")
        departments = cursor.fetchall()
        for department in departments:
            st.write("Department ID:", department[0])
            st.write("Department Name:", department[1])
            st.write("-----------------------------------")

    elif menu == "Add Department":
        st.subheader("Add Department")
        department_id = st.number_input("Department ID")
        name = st.text_input("Name")
        if st.button("Add"):
            cursor.execute("INSERT INTO Departments (DepartmentID, Name) VALUES (%s, %s)", (department_id, name))
            conn.commit()
            st.success("Department added successfully")

    elif menu == "View Salary":
        st.subheader("View Salary Records")
        cursor.execute("SELECT s.EmployeeID, e.Name, s.Amount, s.Date FROM Salary s JOIN Employees e ON s.EmployeeID = e.EmployeeID")
        salary_records = cursor.fetchall()
        for record in salary_records:
            st.write("EmployeeID:", record[0])
            st.write("Employee Name:", record[1])
            st.write("Amount:", record[2])
            st.write("Date:", record[3])
            st.write("-----------------------------------")

    elif menu == "Add Salary":
        st.subheader("Add Salary Record")
        employee_id = st.number_input("Employee ID")
        amount = st.number_input("Amount")
        date = st.date_input("Date")
        if st.button("Add"):
            cursor.execute("INSERT INTO Salary (EmployeeID, Amount, Date) VALUES (%s, %s, %s)", (employee_id, amount, date))
            conn.commit()
            st.success("Salary record added successfully")

    # elif menu == "View Attendance":
    #     st.subheader("View Attendance Records")
    #     cursor.execute("SELECT a.EmployeeID, e.Name, a.Date, a.Status FROM Attendance a JOIN Employees e ON a.EmployeeID = e.EmployeeID")
    #     attendance_records = cursor.fetchall()
    #     for record in attendance_records:
    #         st.write("EmployeeID:", record[0])
    #         st.write("Employee Name:", record[1])
    #         st.write("Date:", record[2])
    #         st.write("Status:", record[3])
    #         st.write("-----------------------------------")
    elif menu == "View Attendance":
        st.subheader("View Attendance Records")
        employee_id = st.number_input("Enter Employee ID")
        if st.button("View Attendance"):
            view_employee_attendance(cursor, employee_id)

    elif menu == "Add Attendance":
        st.subheader("Add Attendance Record")
        employee_id = st.number_input("Employee ID")
        date = st.date_input("Date")
        status = st.selectbox("Status", ["Present", "Absent"])
        if st.button("Add"):
            cursor.execute("INSERT INTO Attendance (EmployeeID, Date, Status) VALUES (%s, %s, %s)", (employee_id, date, status))
            conn.commit()
            st.success("Attendance record added successfully")
        
    elif menu == "Update Employee":
        st.subheader("Update Employee Details")
        employee_id = st.number_input("Enter Employee ID")
        field_to_update = st.selectbox("Select Field to Update", ("Name", "Email", "Department", "Job Title"))
        new_value = None

        if field_to_update == "Name":
            new_value = st.text_input("New Name")
        elif field_to_update == "Email":
            new_value = st.text_input("New Email")
        elif field_to_update == "Department":
            department_options = get_department_options(cursor)
            new_value = st.selectbox("New Department", department_options)
        elif field_to_update == "Job Title":
            new_value = st.text_input("New Job Title")

        if st.button("Update"):
            if new_value is not None:
                if field_to_update == "Department":
                    cursor.execute(f"UPDATE Employees SET {field_to_update} = %s WHERE EmployeeID = %s", (new_value, employee_id))
                else:
                    cursor.execute(f"UPDATE Employees SET {field_to_update.replace(' ', '')} = %s WHERE EmployeeID = %s", (new_value, employee_id))
                conn.commit()
                st.success("Employee details updated successfully")
            else:
                st.warning("Please select a field and provide a new value.")
        
    elif menu == "Delete Employee":
    st.subheader("Delete Employee")
    employee_id = st.number_input("Enter Employee ID")
    if st.button("Delete"):
        try:
            # Delete associated salary records first
            cursor.execute("DELETE FROM Salary WHERE EmployeeID = %s", (employee_id,))
            conn.commit()
            
            # Then delete associated attendance records
            cursor.execute("DELETE FROM Attendance WHERE EmployeeID = %s", (employee_id,))
            conn.commit()
            
            # Finally, delete the employee
            cursor.execute("DELETE FROM Employees WHERE EmployeeID = %s", (employee_id,))
            conn.commit()
            
            st.success("Employee deleted successfully")
        except psycopg2.Error as e:
            st.error(f"Error deleting employee: {e}")

def view_employee_attendance(cursor, employee_id):
    try:
        cursor.execute("SELECT * FROM Attendance WHERE EmployeeID = %s", (employee_id,))
        attendance_records = cursor.fetchall()
        if attendance_records:
            st.write(f"Attendance Records for Employee ID: {employee_id}")
            for record in attendance_records:
                st.write("Date:", record[1])
                st.write("Status:", record[2])
                st.write("-----------------------------------")
        else:
            st.write("No attendance records found for the specified employee.")
    except psycopg2.Error as e:
        st.error(f"Error retrieving attendance records: {e}")

def get_department_options(cursor):
    try:
        cursor.execute("SELECT Name FROM Departments")
        departments = cursor.fetchall()
        return [dept[0] for dept in departments]
    except psycopg2.Error as e:
        st.error(f"Error retrieving department options: {e}")
