from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.parser_en import (
    tag_for_parser,
    parse_sentence,
    ParseError,
    TAG_DESCRIPTIONS,
)

console = Console()
app = typer.Typer(help="Runner de pruebas para el mini-parser de inglés.")


try:
    import spacy

    try:
        NLP = spacy.load("en_core_web_sm")
    except OSError:
        console.print(
            "[yellow]Modelo spaCy 'en_core_web_sm' no encontrado.[/yellow]"
        )
        console.print(
            "Instálalo con:\n  [cyan]python -m spacy download en_core_web_sm[/cyan]"
        )
        NLP = None
except Exception:
    NLP = None


@app.command()
def run(
    folder: str = typer.Argument(
        "test",
        help="Carpeta con archivos .txt (una oración por archivo).",
    )
) -> None:
    path = Path(folder)

    if not path.exists() or not path.is_dir():
        console.print(f"[red]La carpeta '{folder}' no existe o no es un directorio.[/red]")
        raise typer.Exit(code=1)

    files = sorted(path.glob("*.txt"))
    if not files:
        console.print(f"[yellow]No se encontraron archivos .txt en '{folder}'.[/yellow]")
        raise typer.Exit(code=0)

    for file in files:
        text = file.read_text(encoding="utf-8").strip()

        console.rule(f"[bold cyan]{file.name}[/bold cyan]")

        if not text:
            console.print("[red]Archivo vacío.[/red]")
            continue

        console.print(Panel(text, title="Texto de entrada", expand=False))

        tokens = tag_for_parser(text)
        table = Table("Token", "Etiqueta (POS)", "Descripción")
        for tok in tokens[:-1]:
            desc = TAG_DESCRIPTIONS.get(tok.pos, "")
            table.add_row(tok.word, tok.pos, desc)

        console.print("\n[bold]Tokens y POS usados por el parser[/bold]")
        console.print(table)

        try:
            tree = parse_sentence(text)
            console.print("\n[green]✓ Oración ACEPTADA por el parser recursivo[/green]")
            console.print(
                Panel(tree.pretty(), title="Árbol sintáctico (SVO simplificado)", expand=False)
            )
        except ParseError as e:
            console.print("\n[red]✗ Oración RECHAZADA por el parser[/red]")
            console.print(f"[red]Motivo:[/red] {e}")

        if NLP is not None:
            doc = NLP(text)
            t2 = Table("Token", "POS", "Dep", "Head")
            for tok in doc:
                t2.add_row(tok.text, tok.pos_, tok.dep_, tok.head.text)
            console.print("\n[bold]Análisis spaCy (modelo en_core_web_sm)[bold]")
            console.print(t2)

        console.print()


if __name__ == "__main__":
    app()
