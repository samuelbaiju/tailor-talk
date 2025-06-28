import streamlit as st
import requests

st.set_page_config(page_title="TailorTalk AI", layout="centered")

st.title("🤖 TailorTalk - AI Meeting Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

for msg in st.session_state.chat:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Ask me to schedule something...")

if prompt:
    st.session_state.chat.append({"role": "user", "content": prompt})
    res = requests.post("https://tailor-talk-93qz.onrender.com/chat/", json={"message": prompt})
    reply = res.json()["response"]
    st.session_state.chat.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)