import json
import os
import re
from pathlib import Path
from typing import Any

import streamlit as st


BASE_DIR = Path(__file__).parent
KB_PATH = BASE_DIR / "knowledge_base.json"


@st.cache_data
def load_knowledge_base() -> list[dict[str, Any]]:
    with KB_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))


def find_local_answer(question: str, entries: list[dict[str, Any]]) -> tuple[str, str, int]:
    question_words = tokenize(question)
    best_entry: dict[str, Any] | None = None
    best_score = 0

    for entry in entries:
        keyword_words = tokenize(" ".join(entry["keywords"]))
        score = len(question_words & keyword_words)
        if score > best_score:
            best_score = score
            best_entry = entry

    if best_entry and best_score > 0:
        return best_entry["answer"], best_entry["category"], best_score

    return (
        "Mujhe is sawal ka exact answer nahi mila. Admissions, fees, hostel, scholarships, exams ya contact ke baare mein pooch sakte hain.",
        "General",
        0,
    )


def get_openai_answer(question: str, context: str) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": "You are CampusBuddy, a concise and helpful college support assistant. Answer in the user's language. Use only the supplied college context. If context is insufficient, say that the student should contact the college office.",
                },
                {
                    "role": "user",
                    "content": f"College context:\n{context}\n\nStudent question: {question}",
                },
            ],
        )
        return response.choices[0].message.content
    except Exception:
        return None


def answer_question(question: str, entries: list[dict[str, Any]], use_ai: bool) -> tuple[str, str]:
    local_answer, category, score = find_local_answer(question, entries)
    if use_ai:
        context = "\n\n".join(
            f"{entry['category']}: {entry['question']}\n{entry['answer']}" for entry in entries
        )
        ai_answer = get_openai_answer(question, context)
        if ai_answer:
            return ai_answer, "AI assistant"
    return local_answer, category if score else "No match"


def render_message(message: dict[str, str]) -> None:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("meta"):
            st.caption(message["meta"])


def main() -> None:
    st.set_page_config(page_title="CampusBuddy", page_icon="🎓", layout="wide")
    entries = load_knowledge_base()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Namaste! Main CampusBuddy hoon. Admissions, fees, hostel, scholarships aur exams ke baare mein poochiye.",
                "meta": "College help desk",
            }
        ]

    with st.sidebar:
        st.title("🎓 CampusBuddy")
        st.caption("AI College Query Chatbot")
        st.divider()
        st.subheader("Quick questions")
        quick_questions = [
            "Admission kaise le sakta hoon?",
            "B.Tech ki fees kitni hai?",
            "Hostel facility available hai?",
            "Scholarship kaise milegi?",
        ]
        for quick_question in quick_questions:
            if st.button(quick_question, use_container_width=True):
                st.session_state.pending_question = quick_question
        st.divider()
        use_ai = st.toggle("OpenAI mode", value=False, help="OPENAI_API_KEY set hone par answers ko AI se refine karta hai.")
        if use_ai and not os.getenv("OPENAI_API_KEY"):
            st.info("AI mode ke liye OPENAI_API_KEY environment variable set karein. Local FAQ mode active rahega.")
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.title("Your college questions, answered")
    st.write("Hindi ya English mein sawaal poochiye. Aapko instant college information milegi.")

    for message in st.session_state.messages:
        render_message(message)

    pending_question = st.session_state.pop("pending_question", None)
    question = st.chat_input("Example: hostel ki fees kya hai?")
    question = question or pending_question

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        answer, source = answer_question(question, entries, use_ai)
        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "meta": f"Source: {source}"}
        )
        st.rerun()


if __name__ == "__main__":
    main()
