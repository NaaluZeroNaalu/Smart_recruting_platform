import streamlit as st
from langchain_openai.chat_models import ChatOpenAI

# Set your OpenAI API key

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

m = """
   messages -> tablename
   message
   contact
"""

egcode = """

example code 1

import streamlit as st

def Reply():
    
    return your_reply

st.text(Reply())
 

example code 2

import streamlit as st

def Reply():
    colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "black", "white", "brown"]
    return ", ".join(colors)

st.text(Reply())
"""

mes = """
  messages -> table name
    column names:
     contact
     message
"""


sendmes = """
import streamlit as st
import sqlite3

def get_recruiter_info(username):
    conn = sqlite3.connect('datas.db')
    c = conn.cursor()
    
    c.execute("SELECT name, company_name FROM recruiter WHERE user_name = ?", (username,))
    recruiter_info = c.fetchone()
    
    conn.close()
    return recruiter_info

def get_candidates(skill_or_contact):
    conn = sqlite3.connect('datas.db')
    c = conn.cursor()
    
    c.execute(\"\"\"
        SELECT name, contact_no FROM employer 
        WHERE skills LIKE ? OR contact_no = ? OR name = ?
    \"\"\", (f'%{skill_or_contact}%', skill_or_contact, skill_or_contact))
    
    candidates = c.fetchall()
    conn.close()
    
    return candidates

def store_message(contact, message):
    conn = sqlite3.connect('datas.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO messages (contact, message) VALUES (?, ?)", (contact, message))
    conn.commit()
    conn.close()

# Streamlit interface
st.title("Recruiter and Candidate Interaction")

# Assume the recruiter username is stored in session state
recruiter_username = st.session_state.get('user_name')

if recruiter_username:
    recruiter_info = get_recruiter_info(recruiter_username)
    
    if recruiter_info:
        recruiter_name, company_name = recruiter_info
        st.write(f"Recruiter: {recruiter_name}, Company: {company_name}")
        
        skill_or_contact = st.text_input("Enter a skill, contact number, or name to search for candidates:")
        
        if st.button("Search Candidates"):
            candidates = get_candidates(skill_or_contact)
            if candidates:
                for candidate in candidates:
                    candidate_name, candidate_contact = candidate
                    invite_message = f"Hello {candidate_name}, you are invited by {recruiter_name} from {company_name}. Your contact number is {candidate_contact}."
                    store_message(candidate_contact, invite_message)
                    st.write(invite_message)
                st.success("Messages stored successfully.")
            else:
                st.warning("No candidates found.")
    else:
        st.error("Recruiter not found.")
else:
    st.error("No recruiter is logged in.")
"""

mailcode = """
import smtplib
from email.mime.text import MIMEText
import sqlite3
import streamlit as st

# Function to get emails based on skills
def get_emails_by_skills(skill):
    conn = sqlite3.connect('datas.db')
    c = conn.cursor()
    
    # Query to get emails from the employer table where skills match
    c.execute("SELECT email FROM employer WHERE skills LIKE ?", (f'%{skill}%',))
    emails = c.fetchall()  # Fetch all matching emails
    
    conn.close()
    return [email[0] for email in emails]  # Extract email addresses from tuples

# Function to send email
def send_email(recipient_email, invite_text):
    password = "smartai1234"
    email = "samrtairecruit@gmail.com"
    app_password = "twcb lkxn iviy pakp"  # Use the app password here

    msg = MIMEText(invite_text)
    msg["Subject"] = "Invite"
    msg["From"] = email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade to a secure connection
            server.login(email, app_password)  # Login using the app password
            server.sendmail(email, [recipient_email], msg.as_string())  # Send email
            return True  # Return success
    except Exception as e:
        return False, str(e)  # Return failure and error message

# Streamlit interface
st.title("Email Sender")

# Input for skill and invite message
skill_to_search = st.text_input("Enter the skill to search for:")
invite_text = st.text_area("Enter your invite message:")

if st.button("Send Invites"):
    if skill_to_search and invite_text:
        emails = get_emails_by_skills(skill_to_search)
        
        if emails:
            success_count = 0
            failure_messages = []
            for email in emails:
                success = send_email(email, invite_text)
                if success is True:
                    success_count += 1
                else:
                    failure_messages.append(f"Failed to send email to {email}: {success[1]}")
            
            st.success(f"Emails sent successfully to {success_count} recipients!")
            if failure_messages:
                for message in failure_messages:
                    st.error(message)
        else:
            st.warning("No emails found for the specified skill.")
    else:
        st.error("Please provide both skill and invite message.")


"""

# You can now execute this code or save it as needed.



openai_api_key = "sk-nJQLXmWZ_-9G962x-jLziXU-SeurMrtoNaECua2bNBT3BlbkFJuijs5jLfonR02CmOK_QvPXNIDS2zPNtsw-sdA3i2sA"

st.title("AI")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What is up?"):
    try:
        if "shedule" in prompt or "shedule a interview" in prompt or "send a invite message" in prompt:
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
            bot_response = model.invoke(f'from this message {prompt} read skills and generate a Streamlit Python program example like this {mailcode} to get information for specific users mail from table this is table struture {employee}, this is mysqllite database name datas.db and this is your folder structure {folder_structure} note you generate only code').content
            f = open("pages/test.py","w")
            f.write(bot_response.replace('```python', '').replace('```',' '))
            f.close()
            pycode = exec(bot_response.replace('```python', '').replace('```',' '))
        # pycode = exec(bot_response.replace('```python', '').replace('```',' '))
            with st.chat_message("bot"):
                st.markdown("")
            st.session_state.messages.append({"role": "bot", "content":""})
        else:
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    # bot_response = model.invoke(f'Write a Streamlit Python program to create a simple function that returns an answer for this questions like this {egcode}. the question is: {prompt}  and Provide only the code without unnecessary boilerplate. and your are Vidhya and you are controlling my project. my project folder structure{folder_structure} this my database name datas.db and that this is db structure {employee} {forjobs} {recruiter} note answers of all must return using streamlit as text no ui like inputbox your answers mostly based on this project my project is smart recruiting platform if it is general knowledge answer based on that and dont show my project information show only necessary details. the person asking question to you name is {st.session_state.id_name}').content
            bot_response = model.invoke(f'generate a Streamlit Python program example like this {egcode} to reply this question {prompt} don use any streamlit input and button only text, and this is my name {st.session_state.user_name}').content
            f = open("pages/test.py","w")
            f.write(bot_response.replace('```python', '').replace('```',' '))
            f.close()
            pycode = exec(bot_response.replace('```python', '').replace('```',' '))
        # pycode = exec(bot_response.replace('```python', '').replace('```',' '))
            with st.chat_message("bot"):
                st.markdown("")
            st.session_state.messages.append({"role": "bot", "content":""})

    except:
        st.session_state.messages.append({"role": "bot", "content":"sorry i dont understand"})
        with st.chat_message("bot"):
            st.markdown("sorry i dont understand")
        
        
      