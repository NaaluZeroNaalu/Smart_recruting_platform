import streamlit as st


if st.session_state.score < 15:
    st.write("you are selected")
    st.write(st.session_state.score)
else:
    st.write("not selected") 