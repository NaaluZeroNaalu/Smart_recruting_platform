import streamlit as st
import sqlite3 as sqlite
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from pinecone import Pinecone, ServerlessSpec
import pandas as pd
import smtplib
from email.mime.text import MIMEText


def fetch_resumes():
    connection = sqlite.connect("datas.db")
    cursor = connection.cursor()
    cursor.execute("SELECT user_name, resume, email FROM employer WHERE resume IS NOT NULL AND resume != ''")
    resumes = cursor.fetchall()
    connection.close()
    
    # Decode byte resumes to string with error handling
    decoded_resumes = []
    for user_name, resume, email in resumes:
        try:
            decoded_resume = resume.decode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            # Fallback to a different encoding or handle the error
            decoded_resume = resume.decode('latin1', errors='ignore')
        decoded_resumes.append((user_name, decoded_resume, email))
    
    return decoded_resumes

def filter_resumes(df, search_term):
    if search_term:
        filtered_df = df[df['resume'].str.contains(search_term, case=False, na=False)]
        return filtered_df
    return df

def display_resumes(resumes):
    cols = st.columns(3)
    for idx, (user_name, resume, email) in enumerate(resumes):
        with cols[idx % 3]:
            st.write(f"**User Name:** {user_name}")
            st.write(f"**Email:** {email}")
            # Display download button for the resume
            st.download_button(label="Download Resume", data=resume.encode('latin1'), file_name=f"{user_name}_resume.pdf")
            if st.button("View",key=email):
                st.session_state.empview = email
                st.switch_page("pages/view_employee.py")

def display_employee(employee):
    """Display employee details in a visually appealing format."""
    st.markdown(f"**Name:** {employee[1] if employee[1] else 'Not Given'}")
    st.markdown(f"**Skills:** {employee[2] if employee[2] else 'Not Given'}")
    st.markdown(f"**Contact No:** {employee[3] if employee[3] else 'Not Given'}")
    st.markdown(f"**Email:** {employee[4] if employee[4] else 'Not Given'}")
    st.markdown(f"**About:** {employee[6] if employee[6] else 'Not Given'}")
    st.markdown(f"**Location:** {employee[9] if employee[9] else 'Not Given'}")
    if st.button("invite", key=employee[4]):
        openai_api_key = "sk-nJQLXmWZ_-9G962x-jLziXU-SeurMrtoNaECua2bNBT3BlbkFJuijs5jLfonR02CmOK_QvPXNIDS2zPNtsw-sdA3i2sA"
        model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
        bot_response = model.invoke(f'generate a invite message based on this skill {employee[2]}').content
        password = "smartai1234"
        email = "samrtairecruit@gmail.com"
        app_password = "twcb lkxn iviy pakp"  # Use the app password here
        
        msg = MIMEText("ai generated invite text")
        msg["Subject"] = "Invite"
        msg["From"] = email
        msg["To"] = employee[4]
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Upgrade to a secure connection
            server.login(email, app_password)  # Login using the app password
            server.sendmail(email, [employee[4]], msg.as_string())  # Send email
            st.info("invited succesfully")
        except smtplib.SMTPAuthenticationError as e:
            st.info(f"Authentication error: {e}")

    if st.button("View",key=employee[1]):
        st.session_state.empview = employee[4]
        st.switch_page("pages/view_employee.py")
    if employee[7]:  
        resume_data = employee[7]
        resume_filename = f"{employee[1]}_resume.pdf"  
        st.download_button(
            label="Download Resume",
            data=resume_data,
            file_name=resume_filename,
            mime="application/pdf"
        )

    if employee[8]:  
        st.image(employee[8], caption=f"Profile Picture of {employee[1]}")
    
    st.markdown("---")  

recruiter = """
    recruiter -> table name
    column names:
        user_name
        name
        company_name
        contact_no
        email
        password
        about
"""

employee = """
    employer -> table name
    column names:
        user_name
        name
        skills
        contact_no
        email
        password
        about
        resume
        profile_pic
"""

forjobs = """
    jobs -> table name
    column names:
        jobidno
        jobtitle
        skills
        experience
        no_of_vacancies
        salary_range
        workmode
        locations
        address
        contact
        description
        education
        jobtype
        role
        whopost
"""
folder_structure = """
.streamlit/
    config.toml
pages/
    bot.py -> for chat bot
    employee_dashboard.py -> to show employee details
    employee_login.py -> login for employee
    employee_signup.py -> signup for employee
    filter.py -> filter an employee based on criteria given
    job_post.py -> post a specific job for recruiter
    job.py -> search page for jobs for an employee looking for a job
    posted_by_you.py -> this page shows jobs posted by you for recruiters
    recruiter_dashboard.py -> show logged-in recruiter details
    recruiter_login.py -> recruiter login page
    recruiter_signup.py -> recruiter signup page
app.py
datas.db
"""



if st.toggle("Enable AI Search"):
    pc = Pinecone(api_key="4587503a-3e49-492b-986e-7ce25c13c4b0", environment="us-east-1")
    index_name = "myaibrain"
    index = pc.Index(index_name)
    response1 = index.fetch(['projectstructure'])
    openai_api_key = "sk-nJQLXmWZ_-9G962x-jLziXU-SeurMrtoNaECua2bNBT3BlbkFJuijs5jLfonR02CmOK_QvPXNIDS2zPNtsw-sdA3i2sA"
    def generate_response(input_text):
        model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
        prompt = f'Write a Streamlit Python program to create a simple function that returns an answer for this questions without any explanation or boilerplate only code. the question is: {input_text} from my database and show employess username and their contact number as text. my database is mysqllite name datas.db my employer table structure {employee}'
    # st.info(model.invoke(prompt).content) 
        pycode = model.invoke(prompt).content
        st.text(f'{exec(pycode.replace('```python', '').replace('```',' '))}')
    with st.form("my_form"):
        text = st.text_area(
        "Enter text:",
        "i need a employees with skills in python"
    )
        submitted = st.form_submit_button("Submit")
        if not openai_api_key.startswith("sk-"):
            st.warning("Please enter your OpenAI API key!", icon="⚠")
        if submitted and openai_api_key.startswith("sk-"):
            generate_response(text)
else:
    data = fetch_resumes()
    df = pd.DataFrame(data, columns=['user_name', 'resume', 'email'])
    search_term = st.text_input("Search Resumes", "",placeholder="Enter the skills, location)
    
    filtered_df = filter_resumes(df, search_term)
    
    if not filtered_df.empty:
        st.subheader("Available Resumes")
        resumes_to_display = filtered_df.to_numpy()
        display_resumes(resumes_to_display)
    else:
        st.write("No resumes found matching the search criteria.")
