import streamlit as st
import sqlite3 as sqlite

# Function to get table names
def get_table_names(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    cursor.close()
    return [table[0] for table in tables]

# Function to get column names for a table
def get_column_names(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    cursor.close()
    return [column[1] for column in columns]

# Streamlit application
st.title("Database Schema Viewer")

# Database connection
database_path = "datas.db"
connection = sqlite.connect(database_path)

# Get table names
tables = get_table_names(connection)

# Display tables and their columns
if tables:
    st.subheader("Tables and Columns")

    for table in tables:
        st.write(f"**Table:** {table}")
        columns = get_column_names(connection, table)
        if columns:
            st.write("**Columns:**")
            for column in columns:
                st.write(f"- {column}")
        else:
            st.write("No columns found.")
else:
    st.write("No tables found in the database.")

# Close the database connection
connection.close()
