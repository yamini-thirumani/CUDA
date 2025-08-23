import streamlit as st
import requests

st.title("Multi-Agent Planner")

# Input box
user_input = st.text_input("Enter your task or goal:")

# When the button is clicked
if st.button("Submit"):
    if user_input:
        st.write("Planner is processing...")

        try:
            # Make POST request to your FastAPI backend
            response = requests.post(
                "http://103.44.2.84:8000/planner",  # Replace with actual server IP if needed
                json={"text": user_input}
            )

            if response.status_code == 200:
                data = response.json()
                st.success("Plan Generated:")
                st.write(data["output"])
            else:
                st.error(f"Failed to generate plan. Status Code: {response.status_code}")
        except Exception as e:
            st.error(f"Error occurred: {e}")
    else:
        st.warning("Please enter a task.")
