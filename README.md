# CampusGuide

CampusGuide is an offline-first Streamlit chatbot for resolving common college questions. It answers from a local JSON knowledge base, shows the responsible office for each answer, and offers related questions when a match is found.

## Features

- Admissions, deadlines, fees, scholarships, housing, library, academics, transcripts, and IT support answers
- Lightweight keyword and intent matching with a transparent confidence threshold
- No paid API, account, database, or secret required
- Staff-editable FAQ content in `data/faq.json`
- Automated tests for matching and fallback behavior

## Run locally

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit. To run the tests:

```powershell
pytest
```

To add or update an answer, edit `data/faq.json` and restart Streamlit.
