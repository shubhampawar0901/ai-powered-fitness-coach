import streamlit as st
import requests

st.set_page_config(page_title="AI Fitness Coach", page_icon="💪")

st.title("AI Fitness chatbot")

API_BASE_URL = "http://localhost:8000"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []

def login(username, password):
    response = requests.post(f"{API_BASE_URL}/auth/login", json={"username": username, "password": password})
    return response.status_code == 200

def ask_question(query):
    response = requests.post(f"{API_BASE_URL}/chat/ask", json={"query": query})
    if response.status_code == 200:
        return response.json()["response"]
    
    return "Error: Unable to get response"

if not st.session_state.logged_in:
    st.subheader("Login")

    username = st.text_input("Username")

    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")
else:
    st.sidebar.button("Logout", on_click=lambda: setattr(st.session_state, 'logged_in', False))

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about fitness, nutrition, or exercises..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = ask_question(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})