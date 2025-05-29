import streamlit as st
import requests
import os

# Get API endpoint from environment variable or use default
API_ENDPOINT = os.getenv("DOCSIS_TOOLS_API_ENDPOINT", "https://docsis-tools-api.onrender.com/process-ecn")
LOCAL_API_ENDPOINT = "http://127.0.0.1:8002/process-ecn"
IS_DEVELOPMENT = os.getenv("DOCSIS_TOOLS_ENV", "production").lower() == "development"

def show_ecn_tool():
    st.title("📄 DOCSIS ECN Analyzer")

    st.markdown(
        """
        Upload a DOCSIS ECN `.docx` file.  
        This tool scans **tracked changes** (insertions and deletions) and extracts paragraphs that contain the selected keywords.  
        **Note:** Keywords are matched at the **paragraph level**, not individual sentences.
        """
    )

    # Only show API endpoint input in development mode
    if IS_DEVELOPMENT:
        api_url = st.text_input("🔗 API Endpoint (FastAPI backend)", value=LOCAL_API_ENDPOINT)
    else:
        api_url = API_ENDPOINT

    keywords = st.text_input("🔍 Keywords (comma-separated)", value="MUST,SHOULD,MAY")
    case_sensitive = st.checkbox("Case sensitive match", value=True)
    whole_word = st.checkbox("Match whole words only", value=True)

    st.markdown("### 📥 Try with a Sample ECN File")
    try:
        with open("examples/sample_ecn.docx", "rb") as sample_file:
            st.download_button(
                label="📄 Download Sample ECN DOCX File",
                data=sample_file,
                file_name="sample_ecn.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    except FileNotFoundError:
        st.warning("Sample file not found in /examples")

    st.markdown("---")

    uploaded_file = st.file_uploader("📁 Upload your ECN .docx file", type=["docx"])

    if uploaded_file and st.button("🚀 Analyze ECN"):
        with st.spinner("Analyzing ECN..."):
            headers = {}
            try:
                headers["x-api-key"] = st.secrets["API_KEY"]
            except Exception:
                pass  # No API key available, skip
                
            response = requests.post(
                api_url,
                headers=headers,
                files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
                data={
                    "keywords": keywords,
                    "case_sensitive": str(case_sensitive).lower(),
                    "whole_word": str(whole_word).lower()
                },
            )

            if response.status_code == 200:
                st.success("✅ ECN processed successfully!")
                st.download_button(
                    label="⬇️ Download Excel Output",
                    data=response.content,
                    file_name=f"{uploaded_file.name}_ecn_analysis.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error(f"❌ Failed to process ECN. Status code: {response.status_code}")
