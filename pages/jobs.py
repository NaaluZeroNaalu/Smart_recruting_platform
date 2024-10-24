import streamlit as st
import sqlite3 as sqlite
from datetime import datetime


st.write(st.session_state.user_name)
def applied(informations):
    try:
        connection = sqlite.connect("datas.db")
        cursor = connection.cursor()
        
        cursor.execute("""
            INSERT INTO applies (jobno, informations) 
            VALUES (?, ?)
        """, (st.session_state.id_name,informations))
        
        st.write("created successfully")
    
    except Exception as e:
        st.write(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()

def display_job(job):
    """Display job details in a visually appealing format."""
    st.subheader(f"JOB TITLE: {job[1]}")
    st.markdown(f"**Skills required:** {job[2]}")
    st.markdown(f"**Location:** {job[3]}")
    st.markdown(f"**Company:** {job[4]}")
    st.markdown(f"**Salary:** {job[5]}")
    st.markdown(f"**Posted On:** {job[6]}")
    st.markdown(f"**Type:** {job[7]}")
    st.markdown(f"**Requirements:** {job[8]}")
    st.markdown(f"**Contact:** {job[9]}")
    st.markdown(f"**Email:** {job[14]}")

    if st.button("Apply", type="primary",key=job[0]):
        st.session_state.skr = job[2]  # Store skills in session state

        # Prepare the information string
        informations = f"{job[1]}, {job[2]}, {job[3]}, {job[4]}, {job[5]}, {job[6]}, {job[7]}, {job[8]}, {job[9]}"
        
        try:
            connection = sqlite.connect("datas.db")
            cursor = connection.cursor()
            now = datetime.now()
            formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
            # Use parameterized query to prevent SQL injection
            cursor.execute("""
                INSERT INTO applies (jobno, informations, idno,date, postedby, applyer_name) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (job[0], informations, st.session_state.id_name, formatted_now, job[14], st.session_state.user_name))
            
            connection.commit()
            st.success("You have successfully applied for the job. Further details will be shared via your email.")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
        
        finally:
            cursor.close()
            connection.close()

        # Redirect to the interview page
        st.switch_page("pages/interview.py")
    
    st.markdown("---")



try:
    connection = sqlite.connect("datas.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    if jobs:
        st.title("Available Jobs")

        
        job_titles = sorted(set(job[1] for job in jobs))
        locations = sorted(set(job[3] for job in jobs))

        selected_title = st.selectbox("Select Job Title:", ["All"] + job_titles)
        selected_location = st.selectbox("Select Location:", ["All"] + locations)

        
        filtered_jobs = [
            job for job in jobs
            if (selected_title == "All" or job[1] == selected_title) and
               (selected_location == "All" or job[3] == selected_location)
        ]

        if filtered_jobs:
            cols = st.columns(2)  
            for idx, job in enumerate(filtered_jobs):
                with cols[idx % 2]:  
                    display_job(job) 
        else:
            st.write("No jobs found matching your criteria.")

    else:
        st.write("No jobs found.")

    cursor.close()
    connection.close()
except Exception as e:
    st.error(f"An error occurred: {e}")
