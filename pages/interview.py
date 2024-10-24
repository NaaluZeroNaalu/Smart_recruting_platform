import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
import json
import pandas as pd
import sqlite3 as sqlite

# Set your OpenAI API key
openai_api_key = "sk-nJQLXmWZ_-9G962x-jLziXU-SeurMrtoNaECua2bNBT3BlbkFJuijs5jLfonR02CmOK_QvPXNIDS2zPNtsw-sdA3i2sA"

model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)

@st.dialog("Edit Details")
def Displayresult():
    # st.write(st.session_state.score)
    
    try:
        connection = sqlite.connect("datas.db")
        cursor = connection.cursor()
        
        if st.session_state.score < 15:
            st.write("Sorry, you did not pass the test.")
            cursor.execute("UPDATE applies SET status = ? WHERE idno = ?", ("not selected", st.session_state.id_name))
            st.write("You have been marked as not selected. Other details will be shared through your mail.")
        else:
            cursor.execute("UPDATE applies SET status = ? WHERE idno = ?", ("selected", st.session_state.id_name))
            st.write("Congratulations! You have been marked as selected. Further details will be shared through your mail.")
        
        connection.commit()
        
        # Button to navigate back to the profile
        if st.button("Back to profile"):
            st.switch_page("pages/employee_dashboard.py")

    except Exception as e:
        st.error(f"An error occurred: {e}")

    finally:
        cursor.close()
        connection.close()


    

st.session_state.score = 0
topic = st.session_state.skr
st.write(f"Generate 20 interview questions and answers  {topic} in JSON format with choices. No comments or explanations.")
try:
    if 'sk' in st.session_state:
        # Check if questions have been generated
        if 'questions_df' not in st.session_state:
            # Generate MCQs based on the skill in session state
            bot_response = model.invoke(
                f"Generate 20 interview questions and answers from {topic} in JSON format with choices. No comments or explanations."
            ).content
            
            # Load the JSON response
            try:
                data = json.loads(bot_response)
            except json.JSONDecodeError:
                st.error("Failed to decode JSON response. Please check the API response.")
                st.write(bot_response)  # Show the raw response for debugging
                st.stop()

            # Check if data is in expected format
            if isinstance(data, list):
                questions = data  # If it's a list, use it directly
            elif isinstance(data, dict):
                questions = data.get("interview_questions", [])
            else:
                st.error("Unexpected format in JSON response. Please check the API response.")
                st.stop()

            # Convert to DataFrame
            st.session_state.questions_df = pd.DataFrame(questions)
            st.session_state.score = 0  # Initialize score

        # Retrieve the questions DataFrame
        questions_df = st.session_state.questions_df

        # Check if there are questions available
        if questions_df.empty:
            st.error("No questions were generated. Please try again.")
        else:
            st.write("Ok lets start the interview please answer the genearted quetsions")

            # Loop through questions and display them
            for index, row in questions_df.iterrows():
                # Assuming choices is a string; split it into a list
                choices = row['choices'].split(',') if isinstance(row['choices'], str) else row['choices']

                # Display the question
                st.write(f"**{index + 1}. {row['question']}**")

                # Display choices as radio buttons
                selected_option = st.radio(f"Choose an answer for question {index + 1}:", choices, key=f'option_{index}')

                # Check if the selected option is correct
                if selected_option == row['answer']:
                    st.session_state.score += 1

            # Submit button to calculate score
            if st.button("Submit"):
                # st.write(f"Your score is: {st.session_state.score} out of {len(questions_df)}")
                Displayresult()
                st.session_state.score = 0
              
    else:
        st.error("Session state 'sk' not found. Please set it before running this query.")

except Exception as e:
    st.error(f"An error occurred: {e}")