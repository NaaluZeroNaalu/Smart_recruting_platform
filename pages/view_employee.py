import streamlit as st
import sqlite3 as sqlite
from langchain_openai.chat_models import ChatOpenAI
import smtplib
from email.mime.text import MIMEText

if st.button("Back"):
    st.switch_page("pages/recruiter_dashboard.py")

@st.dialog("Need some details")
def Shedule(mail, company, name):
    date = st.date_input("Select a date")
    hr = st.selectbox("Select hour", list(range(12)))
    minute = st.selectbox("Select minutes", list(range(60)))
    ap = st.selectbox("Select AM/PM", ['AM','PM'])
    if st.button("Send a mail", use_container_width=True, type="primary"):
        openai_api_key = "sk-nJQLXmWZ_-9G962x-jLziXU-SeurMrtoNaECua2bNBT3BlbkFJuijs5jLfonR02CmOK_QvPXNIDS2zPNtsw-sdA3i2sA"
        model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
        bot_response = model.invoke(f'generate a invite message for {name}  company name {company}, date{date}, time{hr}{minute}{ap}').content
        password = "smartai1234"
        email = "samrtairecruit@gmail.com"
        app_password = "cjdy swph btej jhlg"  # Use the app password here
        
        msg = MIMEText(bot_response)
        msg["Subject"] = "Invite"
        
        msg["From"] = email
        msg["To"] = mail
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Upgrade to a secure connection
                server.login(email, app_password)  # Login using the app password
                server.sendmail(email, mail, msg.as_string())  # Send email
                st.info("invited succesfully")
        except smtplib.SMTPAuthenticationError as e:
            st.info(f"Authentication error: {e}")

# def update_status():
#     try:
#         connection = sqlite.connect("datas.db")
#         cursor = connection.cursor()
        
#         cursor.execute("UPDATE applies SET status = 'contacted by email' WHERE applyer_name = ?", (name,))
        
        
#         cursor.close()
#         connection.close()
#     except Exception as e:
#         st.error(f"An error occurred: {e}")


def display_user_profile():
    try:
        connection = sqlite.connect("datas.db")
        cursor = connection.cursor()
        a = st.session_state.empview
        cursor.execute("SELECT * FROM employer WHERE email = ?", (a,))
        user = cursor.fetchall()

        if user:
            user_info = user[0]
            st.write(user_info[0])  # Display user name or ID (customize as needed)

            # About Section
            if not user_info[6]:  
                st.text("Not given")
            else:
                st.write(user_info[6])
               

            # Skills Section
            if not user_info[2]:  # Check if Skills is None or empty
                st.text("Skills not mentioned")
            else:
                st.write(user_info[2])
                st.session_state.sk = user_info[2]
                
            # Contact Section
            if not user_info[3]:  # Check if Contact is None or empty
                st.text("No contact given")
            else:
                st.write(user_info[3])
                
            # Email Section
            if not user_info[4]:  # Check if Email is None or empty
                st.text("No email given")
                  
            else:
                st.write(user_info[4])
                
            # Resume Section
            if user_info[7] is None or user_info[7] == "":  # Check if Resume is None or empty
                st.text("No Resume")
                    
            else:
                if st.button("View Resume"):
                    resume_data = download_resume(st.session_state.id_name)
                    if resume_data:
                        st.download_button("Download Resume", resume_data, "resume.pdf")
            if st.button("Shedule a interview", use_container_width=True, type="primary"):
                Shedule(user_info[4],st.session_state.company_name , user_info[0])
        else:
            st.write("No user found.")

        cursor.close()
        connection.close()
    except Exception as e:
        st.error(f"An error occurred: {e}")

display_user_profile()


