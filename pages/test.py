import streamlit as st
from datetime import datetime, timedelta

# Set the title of the app
st.title("Schedule an Interview")

# Create a date input for the user to select a date
selected_date = st.date_input("Select a date", datetime.now())

# Create a time input for hours
hours = st.selectbox("Select hour (IST)", list(range(24)))

# Create a time input for minutes in 15-minute increments
minutes = st.selectbox("Select minutes (IST)", [0, 15, 30, 45])

# Combine selected date and time
selected_time = time(hours, minutes)
combined_datetime = datetime.combine(selected_date, selected_time)

# Display the scheduled date and time in 12-hour format
st.write("Scheduled Date and Time (IST):", combined_datetime.strftime('%Y-%m-%d %I:%M:%S %p'))

# Display just the date and time separately if needed
st.write(f"Selected Date: {selected_date}")
st.write(f"Selected Time (IST): {selected_time.strftime('%I:%M:%S %p')}")
