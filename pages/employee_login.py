import streamlit as st
import sqlite3 as sqlite

# Forgot Password functionality
def show_forgot_password():
    with st.form(key='forgot_password_form'):
        st.header("Forgot password")
        st.write("Enter the email or phone number associated with your account and we'll email you the reset password link.")
        email_or_phone = st.text_input("Email/Phone")
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            st.write(f"Reset password link sent to {email_or_phone}")
            # Add logic here to handle the password reset request

# Layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.header("HEXAWARE")
    st.write("Log In to your account")
    st.write("To continue where you left off, please enter your details")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")  # Mask the password input

    if st.button("Login", use_container_width=True):
        if email == "" or password == "":
            st.warning("Please fill in both fields")
        else:
            try:
                connection = sqlite.connect("datas.db")
                cursor = connection.cursor()

                cursor.execute("SELECT * FROM employer WHERE email = ? AND password = ?", (email, password))
                user = cursor.fetchone()

                if user:
                    st.success("Login successful!")
                    st.session_state.id_name = email  # Store email or username in session state
                    st.session_state.user_name = user[0]  # Store email or username in session state
                    st.session_state.m = user[3]  # Store email or username in session state
                    st.session_state.sk = user[2]
                    st.switch_page("pages/employee_dashboard.py")
                else:
                    st.error("Invalid email or password")

                cursor.close()
                connection.close()
            except Exception as e:
                st.error(f"An error occurred: {e}")

    st.checkbox("Remember Me")

    if st.button("Forgot Password"):
        show_forgot_password()

with col2:
    st.image("login.png")

st.page_link("pages/employee_signup.py",label="Dont have an account")
if st.button("Login as a Recruiter", type="primary"):
    st.switch_page("pages/recruiter_login.py")
            
