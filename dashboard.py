import streamlit as st
import os
import json

st.set_page_config(page_title="SpecDriftBench Dashboard", layout="wide")

st.title("SpecDriftBench")
st.subheader("Evaluating Coding-Agent Reliability Under Changing Requirements")

runs_dir = "runs"

def load_runs():
    runs = []
    if not os.path.exists(runs_dir):
        return runs
        
    try:
        for d in os.listdir(runs_dir):
            trace_file = os.path.join(runs_dir, d, "trace.json")
            if os.path.exists(trace_file):
                with open(trace_file, "r") as f:
                    try:
                        runs.append(json.load(f))
                    except json.JSONDecodeError:
                        pass
    except Exception as e:
        st.error(f"Error loading runs: {e}")
        
    return runs

runs = load_runs()

if not runs:
    st.warning("No experimental results available. Run `specdrift run <task>` to generate data.")

st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to", 
    ["Overview", "Leaderboard", "Task Explorer", "Drift Analysis", "Agent Trace", "Failure Analysis"]
)

if page == "Overview":
    st.header("Overview")
    if runs:
        st.metric("Total Runs", len(runs))
    st.write("This dashboard provides insights into agent performance when exposed to requirement drift.")
    
elif page == "Leaderboard":
    st.header("Leaderboard")
    if runs:
        st.write("Mock Leaderboard data:")
        st.dataframe([{"Agent": r["metadata"]["agent_name"], "Task": r["metadata"]["task_id"], "Run": r["metadata"]["run_id"]} for r in runs])
    else:
        st.write("No experimental results available.")

elif page == "Task Explorer":
    st.header("Task Explorer")
    if os.path.exists("tasks"):
        task_dirs = [d for d in os.listdir("tasks") if os.path.isdir(os.path.join("tasks", d))]
        if task_dirs:
            selected_task = st.selectbox("Select Task", task_dirs)
            task_path = os.path.join("tasks", selected_task, "task.yaml")
            if os.path.exists(task_path):
                with open(task_path, "r") as f:
                    st.code(f.read(), language="yaml")
        else:
            st.write("No tasks found.")
            
elif page == "Drift Analysis":
    st.header("Drift Analysis")
    st.write("Analysis of drift types (e.g. REQUIREMENT_DRIFT vs API_DRIFT) across tasks.")
    if not runs:
        st.write("No experimental results available.")

elif page == "Agent Trace":
    st.header("Agent Trace")
    if not runs:
        st.write("No traces available.")
    else:
        selected_run = st.selectbox("Select Run", [r["metadata"]["run_id"] for r in runs])
        run_data = next((r for r in runs if r["metadata"]["run_id"] == selected_run), None)
        if run_data:
            st.json(run_data)

elif page == "Failure Analysis":
    st.header("Failure Analysis")
    st.write("Categories: DRIFT_NOT_DETECTED, REGRESSION, etc. (automated_failure_classification)")
    if not runs:
        st.write("No experimental results available.")
