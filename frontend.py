import streamlit as st
import requests

st.set_page_config(
    page_title="AI Task Planner",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    div[data-testid="stContainer"] {
        background-color: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
    }
    h1, h3, h2 {
        color: #60a5fa !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ AI Agent Task Planner")
st.write("Construct your execution pipeline and send it straight to the FastAPI backend")

if "steps_list" not in st.session_state:
    st.session_state.steps_list = []

with st.container():
    st.subheader("🎯 Step 1: Define Your Goal & Settings")
    user_goal = st.text_input("Ultimate Agent Goal", placeholder="e.g., Create a 3 page portfolio website")
    temperature = st.slider("Model Temperature (Creativity):", min_value=0.1, max_value=1.0, step=0.1)

st.write("")

with st.container():
    st.subheader("📋 Step 2: Build Your Task Pipeline")
    current_step_id = len(st.session_state.steps_list) + 1
    col1, col2 = st.columns([2, 1])

    with col1:
        action = st.text_input(f"Action for Step {current_step_id}: ",placeholder="e.g., Generate HTML boilerplate code")

    with col2:
        tools = st.text_input(f"Tools for Step {current_step_id}: ", placeholder="e.g., web_search")
    
    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:

        if st.button("➕ Add Step to Plan", use_container_width=True):

            if len(action) >= 5 and tools:
                st.session_state.steps_list.append({
                    "step_id": current_step_id,
                    "action": action,
                    "tools_required": tools
                })
                
                st.success(f"Added Step {current_step_id}!")
                st.rerun()

            else:
                st.error("Action must be atleast 5 characters long and tool is required.")

    with btn_col2:

        if st.button("🗑️ Clear All Steps", use_container_width=True):
            st.session_state.steps_list = []
            st.rerun()

if st.session_state.steps_list:
    st.write("")
    st.subheader("🔍 Current Pipeline Preview")

    for s in st.session_state.steps_list:
        st.code(f"Step {s['step_id']} [{s['tools_required']}]: {s['action']}")
    
    st.divider()

    if st.button("🚀 Run Agent Planner", type="primary", use_container_width=True):

        if len(user_goal) < 10:
            st.error("Goal must be atleast 10 characters long")

        else:

            with st.spinner("Talking to FastAPI Backend..."):
                backend_url = "https://task-planner-vqgi.onrender.com/items/structured/"
                payload = {
                    "agent_request": {
                        "user_goal": user_goal,
                        "temperature": temperature,
                        "planned_steps": st.session_state.steps_list
                    }
                }

                try:
                    response = requests.post(backend_url, json=payload)

                    if response.status_code == 200:
                        data = response.json()
                        report = data["agent_final_report"]

                        st.balloons()
                        st.success("✨ Execution Complete! Final Report Generated:")
                    
                        with st.container():
                            st.markdown(f"### 📝 Summary\n{report['summary']}")
                            st.markdown("### 🔍 Step Breakdown")

                            for step in report["detailed_findings"]:
                                st.write(f"**Step {step['step_id']} ({step['status']}):** {step['findings']}")

                    else:
                        st.error(f"Backend Error: {response.text}")
                
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to FastAPI backend. Is your Uvicorn server running?")
                    
