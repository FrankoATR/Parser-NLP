from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Dict

from .lexico_en import tag_sentence

DETERMINERS = {
    "a",
    "an",
    "the",
    "this",
    "that",
    "my",
    "your",
    "his",
    "her",
    "our",
    "their",
}

PRONOUNS = {
    "i",
    "you",
    "he",
    "she",
    "it",
    "we",
    "they",
}

PREPOSITIONS = {
    "in",
    "on",
    "at",
    "for",
    "to",
    "with",
    "from",
    "between",
    "before",
    "after",
}

TAG_DESCRIPTIONS: Dict[str, str] = {
    "N": "Sustantivo",
    "V": "Verbo",
    "ADJ": "Adjetivo",
    "ADV": "Adverbio",
    "DET": "Determinante / artículo",
    "PRON": "Pronombre",
    "PREP": "Preposición",
    "CONJ": "Conjunción",
    "INTJ": "Interjección",
    "EOF": "Fin de entrada",
    "UNK": "Desconocido (tratado como sustantivo)",
}


@dataclass
class Tok:
    word: str
    pos: str
    index: int


@dataclass
class Node:
    label: str
    children: List["Node"]

    def pretty(self, indent: int = 0) -> str:
        pad = "  " * indent
        if not self.children:
            return f"{pad}{self.label}"
        inner = "\n".join(child.pretty(indent + 1) for child in self.children)
        return f"{pad}{self.label}\n{inner}"


class ParseError(Exception):
    pass


def tag_for_parser(text: str) -> List[Tok]:
    base = tag_sentence(text)
    tokens: List[Tok] = []

    for idx, (word, coarse) in enumerate(base):
        w = word.lower()

        if w in DETERMINERS:
            tag = "DET"
        elif w in PRONOUNS:
            tag = "PRON"
        elif w in PREPOSITIONS:
            tag = "PREP"
        else:
            tag = coarse
            if tag == "UNK":
                if w.endswith("ly"):
                    tag = "ADV"
                else:
                    tag = "N"

        tokens.append(Tok(word=word, pos=tag, index=idx))

    tokens.append(Tok(word="<EOF>", pos="EOF", index=len(tokens)))
    return tokens


class RecursiveDescentParser:
    def __init__(self, tokens: List[Tok]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Tok:
        return self.tokens[self.pos]

    def accept(self, expected: Iterable[str]) -> Tok:
        tok = self.current()
        if tok.pos in expected:
            self.pos += 1
            return tok
        expected_str = "/".join(expected)
        raise ParseError(
            f"Esperaba {expected_str}, encontré {tok.pos} "
            f"('{tok.word}') en posición {tok.index}"
        )

    def parse_S(self) -> Node:
        np = self.parse_NP()
        vp = self.parse_VP()
        return Node("S", [np, vp])

    def parse_NP(self) -> Node:
        tok = self.current()

        if tok.pos == "PRON":
            t = self.accept(["PRON"])
            return Node("NP", [Node(f"{t.word}/{t.pos}", [])])

        children: List[Node] = []

        if self.current().pos == "DET":
            det_tok = self.accept(["DET"])
            children.append(Node(f"{det_tok.word}/{det_tok.pos}", []))

        while self.current().pos == "ADJ":
            adj_tok = self.accept(["ADJ"])
            children.append(Node(f"{adj_tok.word}/{adj_tok.pos}", []))

        n_tok = self.accept(["N"])
        children.append(Node(f"{n_tok.word}/{n_tok.pos}", []))

        return Node("NP", children)

    def parse_VP(self) -> Node:
        children: List[Node] = []

        v_tok = self.accept(["V"])
        children.append(Node(f"{v_tok.word}/{v_tok.pos}", []))

        if self.current().pos in {"DET", "ADJ", "N", "PRON"}:
            obj = self.parse_NP()
            children.append(obj)

        while self.current().pos == "PREP":
            pp = self.parse_PP()
            children.append(pp)

        return Node("VP", children)

    def parse_PP(self) -> Node:
        prep_tok = self.accept(["PREP"])
        np = self.parse_NP()
        return Node("PP", [Node(f"{prep_tok.word}/{prep_tok.pos}", []), np])

    def parse(self) -> Node:
        tree = self.parse_S()
        if self.current().pos != "EOF":
            tok = self.current()
            raise ParseError(
                f"Quedaron tokens sin consumir a partir de "
                f"'{tok.word}' ({tok.pos}) en posición {tok.index}"
            )
        return tree


def parse_sentence(text: str) -> Node:
    tokens = tag_for_parser(text)
    parser = RecursiveDescentParser(tokens)
    return parser.parse()
