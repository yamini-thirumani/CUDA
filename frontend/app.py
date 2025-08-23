import streamlit as st
import requests

BACKEND_URL = "http://103.44.2.84:8000/run-agents" # Adjust if deployed elsewhere

st.set_page_config(page_title="🤖 CUDA Assistant", layout="centered")
st.title("🚀 CUDA - Collaborative Unified Developer Assistant")

input_type = st.radio("🧠 Select Type of Input:", ("Prompt", "Code"))

if input_type == "Prompt":
    prompt_input = st.text_area("💬 Enter your prompt:", placeholder="e.g., Summarize the codebase...")
    if st.button("Send Prompt"):
        st.info("Planner is processing...")
        response = requests.post("http://103.44.2.84:8000/planner", json={"text": prompt_input})
        st.success("✅ Output:")
        st.code(response.json().get("output"))

elif input_type == "Code":
    code_input = st.text_area("👨‍💻 Paste your code:", placeholder="e.g., def hello():\n    print('Hello')")
    if st.button("Send Code"):
        st.info("Processing via CUDA Agents...")
        response = requests.post(BACKEND_URL, json={"code": code_input})
        st.success("✅ Best Agent Output:")
        st.code(response.json()["final_code"])
        st.caption(f"🏆 Winner: {response.json()['winner']}")
        st.info(f"🧾 Reason: {response.json()['reason']}")
