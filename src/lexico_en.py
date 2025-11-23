from __future__ import annotations

import re
from typing import Dict, List, Tuple

TOKEN_RE = re.compile(r"[A-Za-z']+")

LEXICON: Dict[str, str] = {
    # Sustantivos (N)
    "dog": "N",
    "cat": "N",
    "house": "N",
    "bread": "N",
    "music": "N",
    "rule": "N",
    "child": "N",
    "text": "N",
    "end": "N",
    "car": "N",
    "city": "N",
    "day": "N",
    "night": "N",
    "water": "N",
    "book": "N",
    "student": "N",
    "teacher": "N",
    "game": "N",
    "computer": "N",
    "phone": "N",
    "street": "N",
    "world": "N",
    "problem": "N",
    "story": "N",
    "friend": "N",

    # Verbos (V)
    "eat": "V",
    "sleep": "V",
    "run": "V",
    "walk": "V",
    "see": "V",
    "like": "V",
    "love": "V",
    "read": "V",
    "write": "V",
    "play": "V",
    "open": "V",
    "close": "V",
    "study": "V",
    "talk": "V",
    "listen": "V",
    "want": "V",
    "know": "V",
    "make": "V",
    "take": "V",
    "give": "V",
    "come": "V",
    "go": "V",
    "have": "V",
    "say": "V",
    "think": "V",

    # Adjetivos (ADJ)
    "big": "ADJ",
    "small": "ADJ",
    "young": "ADJ",
    "old": "ADJ",
    "happy": "ADJ",
    "sad": "ADJ",
    "red": "ADJ",
    "blue": "ADJ",
    "green": "ADJ",
    "good": "ADJ",
    "bad": "ADJ",
    "new": "ADJ",
    "fast": "ADJ",
    "slow": "ADJ",
    "easy": "ADJ",
    "hard": "ADJ",

    # Adverbios (ADV)
    "quickly": "ADV",
    "slowly": "ADV",
    "today": "ADV",
    "always": "ADV",
}


def tokenize(text: str) -> List[str]:
    return TOKEN_RE.findall(text)


def tag_word(word: str) -> str:
    return LEXICON.get(word.lower(), "UNK")


def tag_sentence(text: str) -> List[Tuple[str, str]]:
    tokens = tokenize(text)
    return [(t, tag_word(t)) for t in tokens]
