import streamlit as st
import sqlite3 as sqlite
from streamlit_navigation_bar import st_navbar
# Custom CSS for styling



st.header("JOB POST")
st.write("Enter the details to post a job")
job_title = st.text_input("JOB TITLE")
skills = st.text_input("SKILLS NEEDED")
experience = st.selectbox("EXPERIENCE NEEDED",("0 - 1", "1 - 2", "2 - 3", "3 - 4", "4 - 5", "5 - 6"))
nov = st.text_input("NUMBER OF VACANCIES")
salary_range = st.selectbox("SALARY RANGE",("0 - 1", "1 - 2", "2 - 3", "3 - 4", "4 - 5", "5 - 6"))
workmode = st.selectbox("WORK MODE",("Office", "Remote", "Hybrid"))
location = st.text_input("LOCATION")
address = st.text_area("ADDRESS")
contact = st.text_input("CONTACT")
description = st.text_area("JOB DESCRIPTION")
education = st.text_input("EDUCATION")
jobtype = st.selectbox("JOB TYPE",("PART-TIME", "FULL-TIME"))
jobrole = st.text_input("ROLE NAME")

if st.button("POST",use_container_width = True, type = "primary"):
    if job_title == "" and skills == "" and experience == "" and nov == "" and salary_range == "" and workmode == "" and location == "" and address == "" and contact == "" and description == "" and education == "" and jobtype == "" and jobrole == "":
            st.write("please fill")
    else:
        try:
            connection = sqlite.connect("datas.db")
            cursor = connection.cursor()

            cursor.execute("INSERT INTO jobs(jobtitle, skills, experience, no_of_vacancies,  salary_range, workmode, location, address, contact, description, education, jobtype, role, whopost) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (job_title,skills, experience, nov, salary_range, workmode, location, address, contact, description, education, jobtype, jobrole,st.session_state.id_name))
            connection.commit()
            st.write("Posted successful!")    
            cursor.close()
            connection.close()
        except Exception as e:
            st.write(f"An error occurred: {e}")
