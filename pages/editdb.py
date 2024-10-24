import streamlit as st
import sqlite3

try:
    # Connect to the database
    connection = sqlite3.connect("datas.db")
    cursor = connection.cursor()

    # Execute the DELETE FROM query
    cursor.execute("delete from applies")

    # Commit the changes
    connection.commit()
    
    st.write("Records deleted successfully")
    
except Exception as e:
    st.write(f"An error occurred: {e}")
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
