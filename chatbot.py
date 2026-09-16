"""Offline question answering for common college queries."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FAQ:
    id: str
    category: str
    question: str
    answer: str
    keywords: tuple[str, ...]
    source: str


@dataclass(frozen=True)
class Response:
    answer: str
    source: str | None
    category: str | None
    confidence: float
    suggestions: tuple[str, ...] = ()


class CollegeAssistant:
    """Match student questions to locally maintained FAQ entries."""

    STOP_WORDS = frozenset(
        {
            "about",
            "are",
            "can",
            "do",
            "does",
            "how",
            "i",
            "is",
            "my",
            "the",
            "what",
            "where",
            "when",
            "which",
            "who",
        }
    )

    def __init__(self, faq_path: str | Path = "data/faq.json") -> None:
        self.faqs = self._load_faqs(Path(faq_path))

    @staticmethod
    def _load_faqs(path: Path) -> tuple[FAQ, ...]:
        with path.open(encoding="utf-8") as file:
            records = json.load(file)
        return tuple(FAQ(**{**record, "keywords": tuple(record["keywords"])}) for record in records)

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return {
            token
            for token in re.findall(r"[a-z0-9]+", text.lower())
            if len(token) > 2 and token not in CollegeAssistant.STOP_WORDS
        }

    def answer(self, query: str) -> Response:
        query_tokens = self._tokens(query)
        if not query_tokens:
            return Response(
                answer="Please enter a question about admissions, fees, courses, housing, campus life, or student support.",
                source=None,
                category=None,
                confidence=0.0,
                suggestions=self.suggest_questions(),
            )

        ranked: list[tuple[float, FAQ]] = []
        for faq in self.faqs:
            keyword_tokens = self._tokens(" ".join(faq.keywords))
            question_tokens = self._tokens(faq.question)
            keyword_hits = query_tokens & keyword_tokens
            question_hits = query_tokens & question_tokens
            score = (len(keyword_hits) * 2 + len(question_hits)) / max(len(query_tokens), 1)
            if query.strip().lower() == faq.question.lower():
                score += 1.0
            ranked.append((score, faq))

        score, match = max(ranked, key=lambda item: item[0])
        if score < 0.34:
            return Response(
                answer="I could not find a confident answer in the college help guide. Try one of the suggested questions, or contact the relevant office for help.",
                source=None,
                category=None,
                confidence=score,
                suggestions=self.suggest_questions(),
            )

        related = tuple(faq.question for faq_score, faq in sorted(ranked, reverse=True, key=lambda item: item[0]) if faq.id != match.id and faq_score >= 0.2)[:3]
        return Response(match.answer, match.source, match.category, min(score, 1.0), related)

    def suggest_questions(self) -> tuple[str, ...]:
        return tuple(faq.question for faq in self.faqs[:4])

    def categories(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(faq.category for faq in self.faqs))
