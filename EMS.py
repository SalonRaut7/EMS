import psycopg2
import streamlit as st

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname='FinalProjectDBMS',
    user='postgres',
    password='salonraut',
    host='localhost',
    port=5432
)
cursor = conn.cursor()

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        admin_login()
    else:
        render_admin_interface()

def admin_login():
    st.title("Employee Management System")
    st.subheader("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")
    login_feedback = st.empty()

    if login_button:
        if username == 'admin' and password == 'admin123':
            st.session_state.authenticated = True
            login_feedback.success("Login successful")
            st.subheader("Admin Interface")
            # Clear login form and feedback messages
            username = ''
            password = ''
            login_feedback.empty()
            render_admin_interface()
        else:
            login_feedback.error("Invalid username or password")



def render_admin_interface():
    menu = st.sidebar.selectbox('Select an Operation', ('View Employees', 'Add Employee', 'View Departments', 'Add Department', 'View Salary', 'Add Salary', 'View Attendance', 'Add Attendance'))

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


    elif menu == "Add Employee":
        st.subheader("Add Employee")
        employee_id = st.number_input("Employee ID")
        name = st.text_input("Name")
        email = st.text_input("Email")
        department = st.text_input("Department")
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

    elif menu == "View Attendance":
        st.subheader("View Attendance Records")
        cursor.execute("SELECT a.EmployeeID, e.Name, a.Date, a.Status FROM Attendance a JOIN Employees e ON a.EmployeeID = e.EmployeeID")
        attendance_records = cursor.fetchall()
        for record in attendance_records:
            st.write("EmployeeID:", record[0])
            st.write("Employee Name:", record[1])
            st.write("Date:", record[2])
            st.write("Status:", record[3])
            st.write("-----------------------------------")



    elif menu == "Add Attendance":
        st.subheader("Add Attendance Record")
        employee_id = st.number_input("Employee ID")
        date = st.date_input("Date")
        status = st.selectbox("Status", ["Present", "Absent"])
        if st.button("Add"):
            cursor.execute("INSERT INTO Attendance (EmployeeID, Date, Status) VALUES (%s, %s, %s)", (employee_id, date, status))
            conn.commit()
            st.success("Attendance record added successfully")

def render_employee_interface():
    st.subheader("Employee Interface")

    # Get employee ID
    employee_id = st.number_input("Enter Employee ID")

    # Display employee details based on ID
    try:
        cursor.execute("SELECT * FROM Employees WHERE EmployeeID = %s", (employee_id,))
        employee = cursor.fetchone()
        if employee:
            st.write("Name:", employee[1])
            st.write("Email:", employee[2])
            st.write("Department:", employee[3])
            st.write("Job Title:", employee[4])
            display_employee_salary(employee_id)
            display_employee_attendance(employee_id)
        else:
            st.error("Employee not found")
    except psycopg2.Error as e:
        st.error(f"Error fetching employee details: {e}")

def display_employee_salary(employee_id):
    # Display employee salary based on ID
    try:
        cursor.execute("SELECT * FROM Salary WHERE EmployeeID = %s", (employee_id,))
        salary_records = cursor.fetchall()
        for record in salary_records:
            st.write("Salary:", record[2])  # Display only the salary amount
    except psycopg2.Error as e:
        st.error(f"Error fetching salary records: {e}")

def display_employee_attendance(employee_id):
    # Display employee attendance based on ID
    try:
        cursor.execute("SELECT * FROM Attendance WHERE EmployeeID = %s", (employee_id,))
        attendance_records = cursor.fetchall()
        for record in attendance_records:
            status = "Present" if record[2] == 1 else "Absent"
            st.write("Attendance Status:", status)  # Display attendance status
            st.write("Date:", record[1])  # Display date of attendance
    except psycopg2.Error as e:
        st.error(f"Error fetching attendance records: {e}")

if __name__ == "__main__":
    main()
