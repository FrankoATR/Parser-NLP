from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable


@dataclass(frozen=True)
class LexiconEntry:
    word: str
    raw_pos: str
    coarse_pos: str


_SIMPLE_WORD_RE = re.compile(r"^[A-Za-z'-]+$")


def map_raw_pos(raw_pos: str) -> str:
    s = raw_pos.strip().strip('"').lower()
    if not s:
        return "UNK"
    if "adv." in s:
        return "ADV"
    if "prep." in s:
        return "PREP"
    if "pron." in s:
        return "PRON"
    if "conj." in s:
        return "CONJ"
    if "interj." in s:
        return "INTJ"
    if "v." in s or "imp." in s or "p. p." in s or "p. pr." in s:
        return "V"
    if "adj." in s or s.startswith("a.") or "superl." in s or "compar." in s:
        return "ADJ"
    if "n." in s or "pl." in s:
        return "N"
    return "UNK"


def is_simple_word(text: str) -> bool:
    return bool(_SIMPLE_WORD_RE.fullmatch(text))


def load_lexicon_from_csv(path: str | Path) -> Dict[str, LexiconEntry]:
    path = Path(path)
    lexicon: Dict[str, LexiconEntry] = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_word = (row.get("Word") or "").strip()
            raw_pos = (row.get("POS") or "").strip()
            if not raw_word:
                continue
            if not is_simple_word(raw_word):
                continue
            coarse = map_raw_pos(raw_pos)
            if coarse == "UNK":
                continue
            key = raw_word.lower()
            if key in lexicon:
                continue
            lexicon[key] = LexiconEntry(word=key, raw_pos=raw_pos, coarse_pos=coarse)
    return lexicon


def save_reduced_lexicon_csv(entries: Iterable[LexiconEntry], out_path: str | Path) -> None:
    out_path = Path(out_path)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "raw_pos", "coarse_pos"])
        for e in entries:
            writer.writerow([e.word, e.raw_pos, e.coarse_pos])
