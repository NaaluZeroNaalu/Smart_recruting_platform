import streamlit as st
# CSS to hide the sidebar


st.page_link("pages/recruiter_login.py",label="RECRUITER")
st.page_link("pages/employee_login.py",label="EMPLOYEE")
st.session_state.enable = "no"