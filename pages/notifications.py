import streamlit as st
import sqlite3 as sqlite



st.header("POST RESPONSES")
try:
    num = 0
    connection = sqlite.connect("datas.db")
    cursor = connection.cursor()
    
    # Use a tuple for the parameter
    cursor.execute("SELECT * FROM applies WHERE postedby = ?", (st.session_state.id_name,))
    users = cursor.fetchall()

    for user in users:
        num = num + 1
        role = user[1].split(",")
        with st.expander(user[6], expanded=True):
            st.write(f"Applied on: {user[4]}") 
            st.write(f"Status: {user[3]}")  
            st.write(f"Application ID: {user[0]}")  # Adjusted label for clarity
            
            if st.button("View", key=num):
                st.session_state.empview = user[2]
                st.session_state.position = user[4]
                st.switch_page("pages/view_employee.py")  # Storing the page switch
            
            if user[0] == "selected":
                if st.button("Schedule an Interview", key=f"schedule_{user[6]}"):
                    st.success("Interview scheduled!")  # Placeholder action
            else:
                st.text("No interview scheduled")

    cursor.close()
    connection.close()
except Exception as e:
    st.error(f"An error occurred: {e}")
