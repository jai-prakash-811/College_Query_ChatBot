from chatbot import CollegeAssistant


def assistant() -> CollegeAssistant:
    return CollegeAssistant("data/faq.json")


def test_answers_admission_question():
    result = assistant().answer("What documents do I need to apply?")
    assert result.category == "Admissions"
    assert "application" in result.answer.lower()
    assert result.source == "Admissions Office"


def test_matches_natural_wording():
    result = assistant().answer("Can I get financial aid or a scholarship?")
    assert result.category == "Fees & Aid"
    assert result.confidence > 0


def test_unknown_question_is_honest():
    result = assistant().answer("What is the weather on Mars?")
    assert result.source is None
    assert "could not find" in result.answer.lower()
    assert result.suggestions


def test_empty_question_has_guidance():
    result = assistant().answer("   ")
    assert result.confidence == 0
    assert result.suggestions
