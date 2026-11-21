import difflib
import os

import requests
import streamlit as st

# set_page_config must be the first Streamlit call on the page
st.set_page_config(page_title="CUDA Assistant", page_icon="🤖", layout="centered")

DEFAULT_BACKEND_BASE = os.getenv("CUDA_BACKEND_URL", "http://127.0.0.1:8000")

st.sidebar.header("Settings")
backend_base = st.sidebar.text_input(
    "Backend URL",
    value=DEFAULT_BACKEND_BASE,
    help="FastAPI base URL (e.g., http://127.0.0.1:8000)",
)
BACKEND_RUN_AGENTS = f"{backend_base}/run-agents"
BACKEND_PLANNER = f"{backend_base}/planner"

AGENT_NAMES = ["fixed", "refactored", "optimized"]


def call_backend(url: str, payload: dict):
    """POST to the backend and return the JSON body, or show an error and return None."""
    try:
        response = requests.post(url, json=payload, timeout=180)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        st.error(f"Unable to reach backend at {url}. Details: {exc}")
        return None


def show_result(data: dict):
    """Render the judge's choice, plus every agent's version with scores and a diff."""
    if "error" in data:
        st.error(data["error"])
        return

    final_code = data.get("final_code", "")
    st.success("✅ Best Agent Output:")
    st.code(final_code or "No output", language="python")
    if data.get("winner"):
        st.caption(f"🏆 Winner: {data['winner']}")
    if data.get("reason"):
        st.info(f"🧾 Reason: {data['reason']}")
    if final_code:
        st.download_button("Download code.py", final_code, file_name="code.py", mime="text/plain")

    versions = data.get("versions", {})
    metrics = data.get("metrics", {})
    baseline = data.get("baseline", "")
    if not versions:
        return

    st.subheader("All agent versions")
    tabs = st.tabs([name.capitalize() for name in AGENT_NAMES])
    for tab, name in zip(tabs, AGENT_NAMES):
        with tab:
            variant_code = versions.get(name, "")
            st.code(variant_code or "No output", language="python")

            m = metrics.get(name)
            if isinstance(m, dict):
                st.markdown(
                    f"- **Correctness**: {m.get('correctness', '-')}\n"
                    f"- **Readability**: {m.get('readability', '-')}\n"
                    f"- **Performance**: {m.get('performance', '-')}\n"
                    f"- **Robustness**: {m.get('robustness', '-')}\n"
                    f"- **Consistency**: {m.get('consistency', '-')}\n"
                    f"- **Total**: {m.get('total', '-')}"
                )
                if m.get("explanation"):
                    st.caption(m["explanation"])

            if baseline and variant_code:
                diff_text = "\n".join(
                    difflib.unified_diff(
                        baseline.splitlines(),
                        variant_code.splitlines(),
                        fromfile="input",
                        tofile=name,
                        lineterm="",
                    )
                )
                if diff_text:
                    with st.expander("Diff vs input"):
                        st.code(diff_text, language="diff")


st.title("🚀 CUDA - Collaborative Unified Developer Assistant")

input_type = st.radio("🧠 Select Type of Input:", ("Prompt", "Code"))

if input_type == "Prompt":
    prompt_input = st.text_area(
        "💬 Enter your prompt:",
        placeholder="e.g., Write a Python function that checks if a number is prime",
    )
    if st.button("Send Prompt") and prompt_input.strip():
        with st.spinner("Planner is generating code and running the agents..."):
            data = call_backend(BACKEND_PLANNER, {"text": prompt_input})
        if data is not None:
            show_result(data)

else:
    code_input = st.text_area(
        "👨‍💻 Paste your code:",
        placeholder="e.g., def divide(a, b):\n    return a / b",
    )
    if st.button("Send Code") and code_input.strip():
        with st.spinner("Processing via CUDA Agents..."):
            data = call_backend(BACKEND_RUN_AGENTS, {"code": code_input})
        if data is not None:
            show_result(data)
