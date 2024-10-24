import streamlit as st
import sqlite3 as sqlite
import pandas as pd

# Connect to the database and fetch resumes
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

# Load resumes from database
data = fetch_resumes()
df = pd.DataFrame(data, columns=['user_name', 'resume', 'email'])

# Function to filter resumes based on search term
def filter_resumes(df, search_term):
    if search_term:
        filtered_df = df[df['resume'].str.contains(search_term, case=False, na=False)]
        return filtered_df
    return df

# Function to display resumes
def display_resumes(resumes):
    cols = st.columns(3)
    for idx, (user_name, resume, email) in enumerate(resumes):
        with cols[idx % 3]:
            st.write(f"**User Name:** {user_name}")
            st.write(f"**Email:** {email}")
            # Display download button for the resume
            st.download_button(label="Download Resume", data=resume.encode('latin1'), file_name=f"{user_name}_resume.pdf")

# Title of the app
st.title("Resume Viewer")

# Search input
search_term = st.text_input("Search Resumes", "")

# Filter resumes based on search input
filtered_df = filter_resumes(df, search_term)

# Display resumes if available
if not filtered_df.empty:
    st.subheader("Available Resumes")
    resumes_to_display = filtered_df.to_numpy()
    display_resumes(resumes_to_display)
else:
    st.write("No resumes found matching the search criteria.")
