# CampusBuddy - AI College Query Chatbot

A bilingual Hindi/English college help-desk chatbot built with Python and Streamlit.

## Run locally

1. Install Python 3.10 or newer.
2. Open PowerShell in this folder.
3. Install dependencies:

```powershell
py -m pip install -r requirements.txt
```

4. Start the app:

```powershell
py -m streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Features

- Hindi and English college queries
- Local FAQ knowledge base with keyword matching
- Quick question buttons
- Chat history and clear chat control
- Optional OpenAI mode using `OPENAI_API_KEY`

To enable AI mode in PowerShell for the current terminal session:

```powershell
$env:OPENAI_API_KEY = "your-api-key"
py -m streamlit run app.py
```

Edit `knowledge_base.json` to add or change college information.
