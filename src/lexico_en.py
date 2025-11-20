from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

import typer
from rich.console import Console
from rich.table import Table

from .lexicon_loader import load_lexicon_from_csv, LexiconEntry


BASE_DIR = Path(__file__).resolve().parents[1]
LEXICON_FILE = BASE_DIR / "data" / "OPTED-Dictionary.csv"

LEXICON: Dict[str, LexiconEntry] = load_lexicon_from_csv(LEXICON_FILE)

WORD_RE = re.compile(r"[A-Za-z']+")

console = Console()
app = typer.Typer(add_completion=False)


def tokenize(text: str) -> List[str]:
    return WORD_RE.findall(text)


def tag_word(word: str) -> str:
    entry = LEXICON.get(word.lower())
    if entry is not None:
        return entry.coarse_pos
    return "UNK"


def tag_sentence(text: str) -> List[Tuple[str, str]]:
    words = tokenize(text)
    return [(w, tag_word(w)) for w in words]


@app.command()
def demo(sentence: str = typer.Argument("", help="Oración en inglés.")) -> None:
    if not sentence:
        sentence = typer.prompt("Oración en inglés")
    tags = tag_sentence(sentence)
    table = Table("Word", "Tag")
    for w, pos in tags:
        table.add_row(w, pos)
    console.print(table)


if __name__ == "__main__":
    app()
