import streamlit as st
import sqlite3 as sqlite


st.header("JOBS YOU APPLIED")
try:
    connection = sqlite.connect("datas.db")
    cursor = connection.cursor()
    
    
    cursor.execute("SELECT * FROM applies")
    users = cursor.fetchall()

   
    for user in users:
        
        
        
        role = user[1].split(",")
        with st.expander(role[0], expanded=True):
            st.write(f"Applied on: {user[4]}") 
            st.write(user[3])  
               
    cursor.close()
    connection.close()
except Exception as e:
    st.error(f"An error occurred: {e}")
