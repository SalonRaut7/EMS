# import streamlit as st
# import psycopg2

# def employee_login(cursor, username, password):
#     try:
#         cursor.execute("SELECT id FROM employee_credentials WHERE username = %s AND password = %s", (username, password))
#         member = cursor.fetchone()
#         return member[0] if member else None
#     except psycopg2.Error as e:
#         st.error(f"Error logging in: {e}")
#         return None

# def employee_signup(cursor, conn, employee_id, username, password):
#     try:
#         cursor.execute("SELECT * FROM employees WHERE employeeid = %s", (employee_id,))
#         if cursor.fetchone() is None:
#             st.error("Employee ID does not exist. Please provide a valid Employee ID.")
#             return False

#         cursor.execute("SELECT * FROM employee_credentials WHERE username = %s", (username,))
#         if cursor.fetchone() is not None:
#             st.error("Username already exists. Please choose a different username.")
#             return False

#         cursor.execute("INSERT INTO employee_credentials (id, username, password) VALUES (%s, %s, %s)", (employee_id, username, password))
#         conn.commit()
#         st.success("Employee signed up successfully!")
#         st.session_state['show_signup'] = False  # Reset the signup state
#         return True
#     except psycopg2.Error as e:
#         conn.rollback()
#         st.error(f"Error signing up employee: {e}")
#         return False
import streamlit as st
import psycopg2

def member_login(cursor, username, password):
    try:
        cursor.execute("SELECT id FROM employee_credentials WHERE username = %s AND password = %s", (username, password))
        member = cursor.fetchone()
        return member[0] if member else None
    except psycopg2.Error as e:
        st.error(f"Error logging in: {e}")
        return None

def member_signup(cursor, conn, member_id, username, password):
    try:
        cursor.execute("SELECT * FROM employees WHERE employeeid = %s", (member_id,))
        if cursor.fetchone() is None:
            st.error("Member ID does not exist. Please provide a valid Member ID.")
            return False

        cursor.execute("SELECT * FROM employee_credentials WHERE username = %s", (username,))
        if cursor.fetchone() is not None:
            st.error("Username already exists. Please choose a different username.")
            return False

        cursor.execute("INSERT INTO employee_credentials (id, username, password) VALUES (%s, %s, %s)", (member_id, username, password))
        conn.commit()
        st.success("Employee signed up successfully!")
        st.session_state['show_signup'] = False  # Reset the signup state
        return True
    except psycopg2.Error as e:
        conn.rollback()
        st.error(f"Error signing up employee: {e}")
        return False
    
def view_employee_information(cursor, employee_id):
    try:
        cursor.execute("SELECT * FROM employees WHERE employeeid = %s", (employee_id,))
        employee_info = cursor.fetchone()
        return employee_info
    except psycopg2.Error as e:
        st.error(f"Error retrieving employee information: {e}")
        return None
def get_employee_salary(cursor, member_id):
    try:
        cursor.execute("SELECT amount FROM salary WHERE employeeid = %s", (member_id,))
        salary = cursor.fetchone()
        return salary[0] if salary else None
    except psycopg2.Error as e:
        st.error(f"Error retrieving employee salary: {e}")
        return None


