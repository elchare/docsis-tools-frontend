import streamlit as st
from ecn_viewer import show_ecn_tool

st.set_page_config(page_title="DOCSIS Tools", layout="wide")

st.sidebar.title("🔧 DOCSIS Tools")
tool = st.sidebar.radio("Select a tool:", ["📄 ECN Analyzer"], key="tool_selector")

if tool == "📄 ECN Analyzer":
    show_ecn_tool()
