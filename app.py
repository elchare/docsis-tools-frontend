import streamlit as st
from ecn_viewer import show_ecn_tool
from spec_diff_viewer import show_spec_diff_tool

st.set_page_config(page_title="DOCSIS Tools", layout="wide")

st.sidebar.title("🔧 DOCSIS Tools")
tool = st.sidebar.radio("Select a tool:", ["📄 ECN Analyzer", "📘 Spec Diff Tool"], key="tool_selector")

if tool == "📄 ECN Analyzer":
    show_ecn_tool()
elif tool == "📘 Spec Diff Tool":
    show_spec_diff_tool()