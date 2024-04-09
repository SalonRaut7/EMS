# import streamlit as st
# from employee_functions import employee_login, employee_signup

# def show_employee_login(cursor, conn):
#     st.title("Employee Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     login_button = st.button("Login")

#     if login_button:
#         employee_id = employee_login(cursor, username, password)
#         if employee_id:
#             st.success("Login successful!")
#             st.session_state['employee_id'] = employee_id
#             st.session_state['logged_in'] = True
#         else:
#             st.error("Invalid username or password")

# def show_employee_signup(cursor, conn):
#     st.title("Employee Sign Up")
#     employee_id = st.number_input("Employee ID", min_value=1, step=1)
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     signup_button = st.button("Sign Up")

#     if signup_button:
#         if employee_signup(cursor, conn, employee_id, username, password):
#             st.session_state['show_signup'] = False
#             st.session_state['employee_id'] = employee_id
#             st.session_state['logged_in'] = True

# def show_employee_interface(cursor, conn):
#     if 'logged_in' not in st.session_state:
#         st.session_state['logged_in'] = False

#     if st.session_state['logged_in']:
#         st.write("Employee interface content goes here...")
#     else:
#         show_employee_login(cursor, conn)
#         st.write("Don't have an account? [Sign up here](/signup)")


import streamlit as st
from datetime import datetime
from employee_functions import view_employee_information, member_signup, get_employee_salary

def show_member_page(cursor, member_id):
    st.title("Employee Page")
    employee_info = view_employee_information(cursor, member_id)
    current_hour = datetime.now().hour
    greeting = "Good morning" if 5 <= current_hour < 12 else "Good afternoon" if 12 <= current_hour < 18 else "Good evening"
    st.subheader(f"{greeting}, {employee_info[1]}!")
    if employee_info:
        st.write(f"Employee ID: {employee_info[0]}")
        st.write(f"Name: {employee_info[1]}")
        st.write(f"Email: {employee_info[2]}")
        st.write(f"Department: {employee_info[3]}")
        st.write(f"Position: {employee_info[4]}")
        salary = get_employee_salary(cursor, member_id)
        if salary is not None:
            st.write(f"Salary: {salary}")
        else:
            st.write("Salary information not available")
    else:
        st.error("Failed to retrieve employee information.")


def member_signup_page(cursor, conn):
    with st.form("member_signup_form"):
        st.write("Employee Sign Up")
        member_id = st.number_input("Employee ID", min_value=1, step=1)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Sign Up")
        if submit_button:
            if member_signup(cursor, conn, int(member_id), username, password):
                st.session_state['signup_success'] = True
                st.session_state['member_id'] = member_id
                st.session_state['username'] = username
                st.session_state['password'] = password

    # Back button
    if st.button("Back"):
        st.session_state['page'] = 'login'
        return  # Return early to prevent further execution of the function

    # Reset the signup state if the back button is not clicked
    if not st.session_state.get('page') == 'login':
        st.session_state['signup_success'] = False



