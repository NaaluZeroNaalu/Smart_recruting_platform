import streamlit as st
import sqlite3 as sqlite
from streamlit_navigation_bar import st_navbar

st.session_state.mno = 0

# page = st_navbar(["You", "Search a job", "You applied", "Logout", "Messages"+ str(st.session_state.mno) if st.session_state.mno > 0 else str("Messages")])
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["You", "Search a job", "Logout", "You applied"],key=1)


@st.dialog("Edit Details")
def Editdetails(detail):
    if detail == "about":
        st.write("About")
        new_about = st.text_area("Enter your new about information:")
        if st.button("Update About"):
            update_detail("about", new_about)

    elif detail == "skills":
        st.write("Skills")
        new_skills = st.text_area("Enter your skills:")
        if st.button("Update Skills"):
            st.session_state.sk = new_skills
            update_detail("skills", new_skills)

    elif detail == "contact":
        st.write("Contact")
        new_contact = st.text_area("Enter your contact number:")
        if st.button("Update Contact"):
            update_detail("contact", new_contact)

    elif detail == "email":
        st.write("Email")
        new_email = st.text_area("Enter your Email:")
        if st.button("Update Email"):
            update_detail("email", new_email)

    elif detail == "resume":
        st.write("Resume section")
        uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
        if st.button("Update Resume"):
            if uploaded_file is not None:
                try:
                    connection = sqlite.connect("datas.db")
                    cursor = connection.cursor()

      
                    file_data = uploaded_file.read()

               
                    cursor.execute("UPDATE employer SET resume = ? WHERE email = ?", (file_data, st.session_state.id_name))
                    connection.commit()
                    st.success("Resume updated successfully")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                finally:
                    cursor.close()
                    connection.close()
            else:
                st.error("Please upload a file.")

def update_detail(column_name, new_value):
    """Helper function to update user details in the database."""
    try:
        connection = sqlite.connect("datas.db")
        cursor = connection.cursor()

        cursor.execute(f"UPDATE employer SET {column_name} = ? WHERE email = ?", (new_value, st.session_state.id_name))
        connection.commit()
        st.success(f"{column_name.capitalize()} updated successfully")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()

def download_resume(email):
    try:
        connection = sqlite.connect("datas.db")
        cursor = connection.cursor()

        cursor.execute("SELECT resume FROM employer WHERE email = ?", (email,))
        resume = cursor.fetchone()

        if resume and resume[0]:
            return resume[0] 
        else:
            st.error("No resume found.")
            return None
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
        cursor.execute("SELECT * FROM employer WHERE email = ?", (a,))
        user = cursor.fetchall()

        if user:
            user_info = user[0]
            st.write(user_info[0])  # Display user name or ID (customize as needed)
         
            # About Section
            if not user_info[6]:  
                if st.button("Tell about something you"):
                    Editdetails("about")
            else:
                st.write(user_info[6])
                

            # Skills Section
            if not user_info[2]:  # Check if Skills is None or empty
                if st.button("Add skills"):
                    Editdetails("skills")
            else:
                st.write(user_info[2])
                st.session_state.sk = user_info[2]
                
            # Contact Section
            if not user_info[3]:  # Check if Contact is None or empty
                if st.button("Add contact"):
                    Editdetails("contact")
            else:
                st.write(user_info[3])
               

            # Email Section
            if not user_info[4]:  # Check if Email is None or empty
                if st.button("Add email"):
                    Editdetails("email")
            else:
                st.write(user_info[4])
                
            # Resume Section
            if user_info[7] is None or user_info[7] == "":  # Check if Resume is None or empty
                if st.button("Add resume"):
                    Editdetails("resume")
            else:
                if st.button("View Resume"):
                    resume_data = download_resume(st.session_state.id_name)
                    if resume_data:
                        st.download_button("Download Resume", resume_data, "resume.pdf")
            with st.expander("EDIT DETAILS",expanded=True):
                if st.button("Edit About"):
                    Editdetails("about")
                if st.button("Edit Skills"):
                    Editdetails("skills")
                if st.button("Edit Contact"):
                    Editdetails("contact")
                if st.button("Edit Email"):
                    Editdetails("email")
              
        else:
            st.write("No user found.")

        cursor.close()
        connection.close()
    except Exception as e:
        st.error(f"An error occurred: {e}")




if page == "You":
    display_user_profile()

elif page == "Search a job":
    exec(open("pages/jobs.py").read())

elif page == "Logout":
    st.session_state.clear()  # Clear session state on logout
    st.switch_page("pages/employee_login.py")

elif page == "You applied":
    exec(open("pages/applies.py").read())


# if page == "Messages"+str(st.session_state.mno) if st.session_state.mno > 0 else str("Messages"):
#     exec(open("pages/employee_messagebox.py").read())
