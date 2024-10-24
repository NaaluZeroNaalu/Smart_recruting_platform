import streamlit as st
import sqlite3 as sqlite


st.markdown(
    '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">',
    unsafe_allow_html=True
)

def display_job(job):
    """Display job details in a visually appealing format with edit and delete buttons."""
    st.markdown(f'<h2 class="text-primary" style="text-align:center;">JOBS POSTED BY YOU</h2>', unsafe_allow_html=True)
    with st.expander(job[1],expanded=True):
        st.subheader(f"JOB TITLE: {job[1]}")
        st.markdown(f"**Skills:** {job[2]}")
        st.markdown(f"**Experience:** {job[3]}")
        st.markdown(f"**Vacancies:** {job[4]}")
        st.markdown(f"**Salary:** {job[5]}")
        st.markdown(f"**Work Mode:** {job[6]}")
        st.markdown(f"**Location:** {job[7]}")
        st.markdown(f"**Address:** {job[8]}")
        st.markdown(f"**Contact:** {job[9]}")
        if st.button(f"Edit Post", key=f"edit_{job[0]}"):
            edit_job()
        if st.button(f"Delete Post", key=f"delete_{job[0]}"):  
            delete_job(job[0]) 
    

    

def delete_job(job_id):
    """Delete the job from the database."""
    try:
        connection = sqlite.connect("datas.db")
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM jobs WHERE jobidno = ?", (job_id,))
        connection.commit()
        
        st.success("Job deleted successfully.")
        cursor.close()
        connection.close()
        
        st.experimental_rerun()
        
    except Exception as e:
        st.error(f"An error occurred while deleting the job: {e}")

def edit_job():
    """Edit job details."""
    st.subheader(f"Editing Job: {job[0]}")
    st.subheader(f"Editing Job: {job[1]}")
    title = st.text_input("Job Title", job[1])
    skills = st.text_area("Skills", job[2])
    experience = st.text_input("Experience", job[3])
    vacancies = st.text_input("Vacancies", job[4])
    salary = st.text_input("Salary", job[5])
    work_mode = st.selectbox("Work Mode", [job[6], "Full-time", "Part-time", "Contract"])
    location = st.text_input("Location", job[7])
    address = st.text_input("Address", job[8])
    contact = st.text_input("Contact", job[9])
    description = st.text_area("Description", job[10])
    
    if st.button("Update Job"):
        update_job(job[0], title, skills, experience, vacancies, salary, work_mode, location, address, contact, description)

def update_job(job_id, title, skills, experience, vacancies, salary, work_mode, location, address, contact, description):
    """Update job details in the database."""
    try:
        connection = sqlite.connect("datas.db")
        cursor = connection.cursor()
        
        cursor.execute("UPDATE jobs SET jobtitle = ?, skills = ?, experience = ?, no_of_vacancies = ?, salary_range = ?, workmode = ?, location = ?, address = ?, contact = ?, description = ? WHERE jobidno = ?", (title, skills, experience, vacancies, salary, work_mode, location, address, contact, description, job_id))
        
        connection.commit()
        st.success("Job updated successfully.")
        cursor.close()
        connection.close()
        
        st.experimental_rerun()
        
    except Exception as e:
        st.error(f"An error occurred while updating the job: {e}")

# Main logic to fetch and display jobs
try:
    connection = sqlite.connect("datas.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM jobs WHERE whopost = ?", (st.session_state.id_name,))
    jobs = cursor.fetchall()

    if jobs:
        st.title("Apply your filter here")

        job_titles = sorted(set(job[1] for job in jobs))
        locations = sorted(set(job[7] for job in jobs))

        selected_title = st.selectbox("Select Job Title:", ["All"] + job_titles)
        selected_location = st.selectbox("Select Location:", ["All"] + locations)

        filtered_jobs = [
            job for job in jobs
            if (selected_title == "All" or job[1] == selected_title) and
               (selected_location == "All" or job[7] == selected_location)
        ]

        if filtered_jobs:
            for job in filtered_jobs:
                display_job(job)  # Assume display_job is a function that formats and displays a job entry
        else:
            st.write("No jobs found matching your criteria.")

    else:
        st.write("No jobs found.")

    cursor.close()
    connection.close()
except Exception as e:
    st.error(f"An error occurred: {e}")
