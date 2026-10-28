from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional
import re


@dataclass(frozen=True)
class IntentResult:
    intent_name: str
    confidence: float


class IntentRule:
    """Base rule interface for intent matching."""

    intent_name: str = "unknown"

    def match(self, text: str) -> Optional[IntentResult]:
        raise NotImplementedError


class KeywordIntentRule(IntentRule):
    """Simple keyword-based intent rule.

    This class makes it easy to add new intents later by creating
    new instances with different keywords and intent names.
    """

    def __init__(self, intent_name: str, keywords: Iterable[str], confidence: float = 0.9):
        self.intent_name = intent_name
        self._keywords = [k.lower().strip() for k in keywords]
        self._confidence = confidence

    def match(self, text: str) -> Optional[IntentResult]:
        normalized = normalize_text(text)
        for kw in self._keywords:
            pattern = rf"\b{re.escape(kw)}\b"
            if re.search(pattern, normalized):
                return IntentResult(intent_name=self.intent_name, confidence=self._confidence)
        return None


class IntentEngine:
    """Intent engine that evaluates rules in order.

    Extendability:
    - Add a new rule to the `rules` list.
    - Replace a rule with an ML/LLM-based rule later, keeping the same interface.
    """

    def __init__(self, rules: List[IntentRule]):
        self.rules = rules

    def detect(self, text: str) -> IntentResult:
        for rule in self.rules:
            result = rule.match(text)
            if result is not None:
                return result
        return IntentResult(intent_name="fallback", confidence=0.0)


def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def build_default_intent_engine() -> IntentEngine:
    appointment_keywords = [
        "cita",
        "turno",
        "agendar",
        "agendo",
        "agenda",
        "reservar",
        "reserva",
        "programar",
        "consulta",
        "appointment",
    ]

    rules: List[IntentRule] = [
        KeywordIntentRule(intent_name="appointment_request", keywords=appointment_keywords),
    ]

    return IntentEngine(rules=rules)
