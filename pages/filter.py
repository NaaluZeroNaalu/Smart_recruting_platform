import sqlite3
import streamlit as st
import openai
from langchain_openai.chat_models import ChatOpenAI


if st.button("BACK TO MY DASHBOARD",type="primary"):
    st.switch_page("pages/recruiter_dashboard.py")



def get_database_connection():
    conn = sqlite3.connect('datas.db')  # Update with your database path
    return conn


def filter_resumes(criteria):
    conn = get_database_connection()
    cursor = conn.cursor()
    
    # SQL query to fetch resumes based on criteria from the 'employer' table
    cursor.execute("SELECT user_name, name, skills, contact_no, email, about FROM employer WHERE skills LIKE ?", (f'%{criteria}%'))
    results = cursor.fetchall()
    conn.close()
    return results


def decode_blob(blob_data):
    return blob_data.decode('utf-8')  


if st.toggle("Enable AI Search", value=True if st.session_state.enable == "yes" else False):
    st.session_state.enable = "yes"
    st.markdown(
    """
   <style>
     [data-testid="stAppViewContainer"] {
      background-image:url('https://cdn.dribbble.com/users/2011679/screenshots/5816471/____2.gif');
      background-size: cover; /* Cover the whole container */
      background-repeat: no-repeat;
      background-attachment: fixed;
      background-position: center;
     }
   </style>
    """,
    unsafe_allow_html=True
)
    st.title("Enhanced With AI Search")
    
    openai_api_key = "sk-nJQLXmWZ_-9G962x-jLziXU-SeurMrtoNaECua2bNBT3BlbkFJuijs5jLfonR02CmOK_QvPXNIDS2zPNtsw-sdA3i2sA"
    def generate_response(input_text):
        model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
        st.info(model.invoke(input_text).content) 
        
    with st.form("my_form"):
        text = st.text_area(

        "Enter text:"
    )
        submitted = st.form_submit_button("Submit")
        if not openai_api_key.startswith("sk-"):
            st.warning("Please enter your OpenAI API key!", icon="⚠")
        if submitted and openai_api_key.startswith("sk-"):
            generate_response(text)
else:
    st.session_state.enable = "no"
    # Streamlit app title
    st.title("Employer Resume Filter")

# User input box for filtering resumes
    user_input = st.text_input("Enter skills or experience to filter resumes:")
    if st.button("Filter Resumes"):
        if user_input:
            resumes = filter_resumes(user_input)
        if resumes:
            st.write("### Filtered Resumes")
            for resume in resumes:
                st.write(f"**ID**: {resume[0]}")
                st.write(f"**Name**: {resume[1]}")
                st.write(f"**Skills**: {resume[2]}")
                st.write(f"**Experience**: {resume[3]}")
                
                # Decode and display the resume content
                resume_content = decode_blob(resume[4])  # Assuming the BLOB is at index 4
                st.text_area("Resume Content", resume_content, height=200)
                st.write("---")
        else:
            st.write("No resumes found matching your criteria.")

# Button to filter resumes

