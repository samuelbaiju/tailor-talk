import streamlit as st
import requests

st.set_page_config(page_title="TailorTalk AI", layout="centered")
st.title("🤖 TailorTalk - AI Meeting Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

# Render chat history
for msg in st.session_state.chat:
    st.chat_message(msg["role"]).write(msg["content"])

# Input from user
prompt = st.chat_input("Ask me to schedule something...")

if prompt:
    st.session_state.chat.append({"role": "user", "content": prompt})
    try:
        # Make POST request to backend
        res = requests.post(
            "https://tailor-talk-93qz.onrender.com/chat/",
            json={"message": prompt},
            timeout=20  # ⏱️ Optional: prevent Streamlit from hanging
        )
        res.raise_for_status()  # raises error for 4xx/5xx responses

        # Try to parse JSON
        try:
            reply = res.json().get("response", "⚠️ No response received from backend.")
        except requests.exceptions.JSONDecodeError:
            reply = "❌ Backend returned non-JSON response. Please try again later."
            st.error("Debug info: " + res.text)

    except requests.exceptions.RequestException as e:
        reply = f"❌ Could not reach the backend: {e}"
        st.error("Make sure your FastAPI backend is running and accessible.")

    # Append assistant reply to chat
    st.session_state.chat.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
# Clear input box after sending