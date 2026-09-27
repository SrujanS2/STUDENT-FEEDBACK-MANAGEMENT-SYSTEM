@echo off
REM One-time setup + run for Windows
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
