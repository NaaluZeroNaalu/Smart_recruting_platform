import streamlit as st
import sqlite3 as sqlite

try:
    connection = sqlite.connect("datas.db")
    cursor = connection.cursor()
    a = st.session_state.id_name
    cursor.execute("SELECT * FROM messages WHERE contact = ?", (st.session_state.m,))
    messages = cursor.fetchall()

    if messages:
           st.info(messages[0])

    else:
        st.info("No message to Show")

    cursor.close()
    connection.close()
except Exception as e:
     st.error(f"An error occurred: {e}")