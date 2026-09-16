from pathlib import Path

import streamlit as st

from chatbot import CollegeAssistant

st.set_page_config(page_title="CampusGuide", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --ink:#17202a; --muted:#66717d; --teal:#0d766d; --mint:#d9f0e9; --cream:#f5f7f9; --line:#dfe4e8; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
.stApp { background: var(--cream); }
[data-testid="stSidebar"] { background: #123b3a; }
[data-testid="stSidebar"] * { color: #eef8f4; }
[data-testid="stSidebar"] .stButton button { background: transparent; border: 1px solid #477a73; text-align: left; }
[data-testid="stSidebar"] .stButton button:hover { background: #1d514e; border-color: #83c6b6; }
.hero { padding: 2rem 0 1.5rem; border-bottom: 1px solid var(--line); }
.eyebrow { color: var(--teal); text-transform: uppercase; letter-spacing: .12em; font-size: .72rem; font-weight: 700; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: var(--ink) !important; }
h1 { font-size: clamp(2rem, 4vw, 3.4rem) !important; line-height: 1.05 !important; margin: .4rem 0 .7rem !important; }
.subtitle { color: var(--muted); max-width: 610px; font-size: 1.05rem; }
.metric { background: white; border: 1px solid var(--line); padding: 1rem; border-radius: 8px; }
.metric strong { display:block; font: 700 1.5rem 'Space Grotesk'; color: var(--teal); }
.metric span { color: var(--muted); font-size:.82rem; }
.chat-label { color: var(--muted); font-size:.82rem; margin: 1.5rem 0 .4rem; }
.answer-meta { color: var(--teal); font-size:.78rem; font-weight:700; text-transform:uppercase; letter-spacing:.08em; }
div[data-testid="stChatMessage"] { border-bottom: 1px solid var(--line); padding-bottom: 1rem; }
.stChatInput { background: white; }
</style>
""", unsafe_allow_html=True)

assistant = CollegeAssistant(Path(__file__).parent / "data" / "faq.json")
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I’m CampusGuide. Ask me about admissions, tuition, courses, housing, or student support."}]

with st.sidebar:
    st.markdown("## CampusGuide")
    st.caption("College query resolution, available whenever you need it.")
    st.divider()
    st.markdown("### Explore topics")
    for category in assistant.categories():
        st.markdown(f"`{category}`")
    st.divider()
    st.caption("Offline knowledge base · No account required")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown('<div class="hero"><div class="eyebrow">Student support desk</div><h1>Answers for your next<br>campus decision.</h1><div class="subtitle">A focused college assistant for the questions that come up before, during, and after enrollment.</div></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
for column, value, label in [(col1, len(assistant.faqs), "verified answers"), (col2, len(assistant.categories()), "support areas"), (col3, "24/7", "available")]:
    with column:
        st.markdown(f'<div class="metric"><strong>{value}</strong><span>{label}</span></div>', unsafe_allow_html=True)

st.markdown('<div class="chat-label">CONVERSATION</div>', unsafe_allow_html=True)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("source"):
            st.caption(f"{message['category']} · Source: {message['source']}")

prompt = st.chat_input("Ask a college question...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    result = assistant.answer(prompt)
    answer = result.answer
    if result.suggestions:
        answer += "\n\n**You could also ask:**\n" + "\n".join(f"- {question}" for question in result.suggestions)
    st.session_state.messages.append({"role": "assistant", "content": answer, "source": result.source, "category": result.category})
    st.rerun()
