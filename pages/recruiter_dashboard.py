import streamlit as st
import sqlite3 as sqlite
from langchain_openai.chat_models import ChatOpenAI

# Load Bootstrap CSS
st.markdown(
    '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">',
    unsafe_allow_html=True
)

# Sidebar for page navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["You", "Post a Job", "Your Posts", "Logout", "Chat with AI", "Recruit a Person", "Notifications"],key=0)

@st.dialog("Edit Details")
def Editdetails(detail):
    if detail == "about":
        st.write("About Me")
        new_about = st.text_area("Enter your new about information:")
        if st.button("Update About"):
            update_detail("about", new_about)
    elif detail == "name":
        st.write("Name")
        new_name = st.text_area("Enter your Name:")
        if st.button("Update Details"):
            update_detail("user_name", new_name)
    elif detail == "skills":
        st.write("Skills")
        new_skills = st.text_area("Enter your Company details:")
        if st.button("Update Details"):
            update_detail("skills", new_skills)
    elif detail == "contact":
        st.write("Contact Information")
        new_contact = st.text_area("Enter your contact number:")
        if st.button("Update Contact"):
            update_detail("contact_no", new_contact)
    elif detail == "email":
        st.write("Email")
        new_email = st.text_area("Enter your Email:")
        if st.button("Update Email"):
            update_detail("email", new_email)

def update_detail(detail_type, new_value):
    try:
        connection = sqlite.connect("datas.db")
        cursor = connection.cursor()
        cursor.execute(f"UPDATE recruiter SET {detail_type} = ? WHERE email = ?", (new_value, st.session_state.id_name))
        connection.commit()
        st.success(f"{detail_type.capitalize()} updated successfully")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()

def display_user_profile():
    try:
        connection = sqlite.connect("datas.db")
        cursor = connection.cursor()
        a = st.session_state.id_name
        cursor.execute("SELECT * FROM recruiter WHERE email = ?", (a,))
        user = cursor.fetchall()

        if user:
            st.markdown(f'<h2 class="text-primary" style="text-align:center;">{user[0][0]}!</h2>', unsafe_allow_html=True)
            # About Section
            st.markdown('<h4 class="mt-4">About You</h4>', unsafe_allow_html=True)
            if not user[0][6]:  # Check if About is None or empty
                if st.button("Tell about something you", key="about_button", type="primary"):
                    Editdetails("about")
            else:
                st.markdown('<div class="row">', unsafe_allow_html=True)
                st.markdown(f'<div class="col-8"><h5>{user[0][6]}</h5></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Skills Section
            st.markdown('<h4 class="mt-4">Company Name</h4>', unsafe_allow_html=True)
            if not user[0][2]:  # Check if Skills is None or empty
                if st.button("Add Company Name", key="add_company_button", type="primary"):
                    Editdetails("skills")
            else:
                st.markdown(f'<h5>Company Name: {user[0][2]}</h5>', unsafe_allow_html=True)
                st.session_state.company_name = user[0][2]
                
            # Contact Section
            st.markdown('<h4 class="mt-4">Contact</h4>', unsafe_allow_html=True)
            if not user[0][3]:  # Check if Contact is None or empty
                if st.button("Add Contact", key="add_contact_button", type="primary"):
                    Editdetails("contact")
            else:
                st.markdown('<div class="row">', unsafe_allow_html=True)
                st.markdown(f'<div class="col-8">{user[0][3]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            # Email Section
            st.markdown('<h4 class="mt-4">Email</h4>', unsafe_allow_html=True)
            if not user[0][4]:  # Check if Email is None or empty
                if st.button("Add Email", key="add_email_button", type="primary"):
                    Editdetails("email")
            else:
                st.markdown('<div class="row">', unsafe_allow_html=True)
                st.markdown(f'<div class="col-8">Your Email: {user[0][4]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with st.expander("EDIT DETAILS",expanded=True):
                if st.button("Edit About"):
                    Editdetails("about")
                if st.button("Edit Company"):
                    Editdetails("skills")
                if st.button("Edit Contact"):
                    Editdetails("contact")
                if st.button("Edit Email"):
                    Editdetails("email")
        else:
            st.write("No user data found.")

  
        cursor.close()
        connection.close()
    except Exception as e:
        st.error(f"An error occurred: {e}")


if page == "You":
    display_user_profile()
elif page == "Post a Job":
    exec(open("pages/job_post.py").read())
elif page == "Your Posts":
    exec(open("pages/posted_by_you.py").read())
elif page == "Chat with AI":
    exec(open("pages/bot.py").read())
elif page == "Recruit a Person":
    exec(open("pages/employees.py").read())
elif page == "Notifications":
    exec(open("pages/notifications.py").read())
elif page == "Logout":
    st.session_state.clear()  # Clear session state on logout
    st.switch_page("pages/recruiter_login.py")

