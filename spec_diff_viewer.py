
import streamlit as st
import requests
import os

# Get API endpoint from environment variable or use default
API_ENDPOINT = os.getenv("DOCSIS_TOOLS_API_ENDPOINT", "https://docsis-tools-api.onrender.com/process")
LOCAL_API_ENDPOINT = "http://127.0.0.1:8002/compare-specs"
IS_DEVELOPMENT = os.getenv("DOCSIS_TOOLS_ENV", "production").lower() == "development"

def show_spec_diff_tool():
    st.title("📘 DOCSIS Spec Diff Tool")

    st.markdown(
        """
        Upload two DOCSIS Specs `.docx` files.  
        This tool scans and compares both documents. It extracts added/changed/deleted paragraphs that contain the selected keywords.  
        **Note:** Keywords are matched at the **paragraph level**, not individual sentences.
        """
    )

    # Only show API endpoint input in development mode
    if IS_DEVELOPMENT:
        api_url = st.text_input("🔗 API Endpoint (FastAPI backend)", value=LOCAL_API_ENDPOINT)
    else:
        api_url = API_ENDPOINT

    with st.form("spec_diff_form"):
        file1 = st.file_uploader("Upload DOCX v01", type=["docx"], key="file1")
        file2 = st.file_uploader("Upload DOCX v03", type=["docx"], key="file2")
        keywords = st.text_input("Keywords (comma-separated)", value="MUST,SHOULD,MAY")

        st.markdown("### Normalization Options")
        normalize_spec_refs = st.checkbox("Normalize spec references (e.g., [MULPIv3.1] → {{MULPI}})", value=True)
        normalize_doc_refs = st.checkbox("Normalize document references (Section/Table/Figure/etc.)", value=True)
        normalize_cosmetic = st.checkbox("Normalize cosmetic changes", value=True)
        normalize_whitespace = st.checkbox("Normalize whitespace", value=True)
        normalize_quotes = st.checkbox("Normalize quotes (curly ↔ straight)", value=True)
        normalize_dashes = st.checkbox("Normalize dashes (– ↔ -)", value=True)

        st.markdown("### Output View")
        show_normalized_output = st.checkbox("Show normalized text in output", value=True)

        submitted = st.form_submit_button("Compare Specs")

    if submitted and file1 and file2:
        with st.spinner("Comparing documents..."):
            headers = {}
            try:
                headers["x-api-key"] = st.secrets["API_KEY"]
            except Exception:
                pass  # No API key available, skip

            files = {
                "file1": (file1.name, file1, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
                "file2": (file2.name, file2, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            }
            data = {
                "keywords": keywords,
                "case_sensitive": "true",
                "whole_word": "true",
                "normalize_spec_refs": str(normalize_spec_refs).lower(),
                "normalize_doc_refs": str(normalize_doc_refs).lower(),
                "normalize_cosmetic": str(normalize_cosmetic).lower(),
                "normalize_whitespace": str(normalize_whitespace).lower(),
                "normalize_quotes": str(normalize_quotes).lower(),
                "normalize_dashes": str(normalize_dashes).lower(),
                "show_normalized_output": str(show_normalized_output).lower(),
            }

            try:
                response = requests.post(api_url, headers=headers, files=files, data=data)
                if response.status_code == 200:
                    st.success("Comparison complete!")
                    st.download_button(
                        label="📥 Download Excel Report",
                        data=response.content,
                        file_name="spec_diff_result.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.error(f"Failed: {response.status_code} - {response.text}")
            except Exception as e:
                st.exception(e)
