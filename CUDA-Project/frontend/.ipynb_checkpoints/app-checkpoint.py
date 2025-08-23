import os
import streamlit as st
import requests

# Backend configuration
DEFAULT_BACKEND_BASE = os.getenv("CUDA_BACKEND_URL", "http://127.0.0.1:8000")

st.sidebar.header("Settings")
backend_base = st.sidebar.text_input("Backend URL", value=DEFAULT_BACKEND_BASE, help="FastAPI base URL (e.g., http://127.0.0.1:8000)")

BACKEND_RUN_AGENTS = f"{backend_base}/run-agents"
BACKEND_PLANNER = f"{backend_base}/planner"

st.set_page_config(page_title="🤖 CUDA Assistant", layout="centered")
st.title("🚀 CUDA - Collaborative Unified Developer Assistant")

input_type = st.radio("🧠 Select Type of Input:", ("Prompt", "Code"))

if input_type == "Prompt":
    prompt_input = st.text_area("💬 Enter your prompt:", placeholder="e.g., Summarize the codebase...")
    if st.button("Send Prompt"):
        try:
            with st.spinner("Planner is processing..."):
                response = requests.post(BACKEND_PLANNER, json={"text": prompt_input}, timeout=120)
                response.raise_for_status()
                data = response.json()
            if "error" in data:
                st.error(data["error"])
            else:
                st.success("✅ Best Agent Output:")
                final_code = data.get("final_code", "")
                st.code(final_code)
                if "winner" in data:
                    st.caption(f"🏆 Winner: {data['winner']}")
                if "reason" in data:
                    st.info(f"🧾 Reason: {data['reason']}")
                if final_code:
                    st.download_button("Download code.py", final_code, file_name="code.py", mime="text/plain")

                # All-variants tabs
                versions = data.get("versions", {})
                metrics = data.get("metrics", {})
                baseline = data.get("baseline", "")
                if versions:
                    st.subheader("Variants")
                    tabs = st.tabs(["Fixed", "Refactored", "Optimized"]) 
                    names = ["fixed", "refactored", "optimized"]
                    for tab, name in zip(tabs, names):
                        with tab:
                            variant_code = versions.get(name, "")
                            st.code(variant_code or "No output")
                            # Scores table
                            if name in metrics and isinstance(metrics[name], dict):
                                m = metrics[name]
                                st.markdown(
                                    f"- **Correctness**: {m.get('correctness','-')}\n"
                                    f"- **Readability**: {m.get('readability','-')}\n"
                                    f"- **Performance**: {m.get('performance','-')}\n"
                                    f"- **Robustness**: {m.get('robustness','-')}\n"
                                    f"- **Consistency**: {m.get('consistency','-')}\n"
                                    f"- **Total**: {m.get('total','-')}\n"
                                )
                                if m.get("explanation"):
                                    st.caption(m["explanation"])

                            # Simple diff vs baseline (line-level)
                            # if baseline and variant_code:
                            #     import difflib
                            #     diff_lines = difflib.unified_diff(
                            #         baseline.splitlines(),
                            #         variant_code.splitlines(),
                            #         fromfile='baseline',
                            #         tofile=name,
                            #         lineterm='' 
                            #     )
                            #     diff_text = "\n".join(diff_lines)
                            #     if diff_text:
                            #         st.text_area("Diff vs baseline", diff_text, height=200)
        except requests.exceptions.RequestException as exc:
            st.error(f"Unable to reach backend at {BACKEND_PLANNER}. Details: {exc}")

elif input_type == "Code":
    code_input = st.text_area("👨‍💻 Paste your code:", placeholder="e.g., def hello():\n    print('Hello')")
    if st.button("Send Code"):
        try:
            with st.spinner("Processing via CUDA Agents..."):
                response = requests.post(BACKEND_RUN_AGENTS, json={"code": code_input}, timeout=120)
                response.raise_for_status()
                data = response.json()
            if "error" in data:
                st.error(data["error"])
            else:
                st.success("✅ Best Agent Output:")
                final_code = data.get("final_code", "")
                st.code(final_code)
                if "winner" in data:
                    st.caption(f"🏆 Winner: {data['winner']}")
                if "reason" in data:
                    st.info(f"🧾 Reason: {data['reason']}")
                if final_code:
                    st.download_button("Download code.py", final_code, file_name="code.py", mime="text/plain")
        except requests.exceptions.RequestException as exc:
            st.error(f"Unable to reach backend at {BACKEND_RUN_AGENTS}. Details: {exc}")
