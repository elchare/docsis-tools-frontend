# 📄 DOCSIS Tools Frontend

This is a unified Streamlit app for DOCSIS-related tools. Currently, it includes an ECN Analyzer that extracts tracked changes from DOCSIS ECN Word files based on user-defined keywords.

## 🚀 Features
- Upload `.docx` ECNs
- Filter by keywords (e.g., MUST, SHOULD, MAY)
- Case sensitivity and whole word options
- Downloads annotated Excel output

## 📁 File Structure
```
docsis-tools-frontend/
├── app.py                # Main Streamlit app
├── ecn_viewer.py         # ECN Analyzer module
├── examples/
│   └── sample_ecn.docx   # Sample DOCX for demo
├── requirements.txt      # Dependencies
└── .streamlit/
    └── (optional) secrets.toml
```

## 🔧 Setup
```bash
git clone https://github.com/yourusername/docsis-tools-frontend.git
cd docsis-tools-frontend
pip install -r requirements.txt
streamlit run app.py
```

## 🌐 Deployment
Deploy on [Streamlit Cloud](https://share.streamlit.io) using `app.py` as the main file. Set your `API_KEY` either in:
- Streamlit Cloud > Settings > Secrets
- or hardcoded into your script (less secure, but supported)

## 🔐 API Authentication
To call your backend securely, pass the API key using a header:
```python
headers={"x-api-key": "YOUR_KEY_HERE"}
```
Update this in `ecn_viewer.py` if not using `st.secrets`.

---

## 📬 Feedback
More tools (e.g., spec comparator) coming soon.
