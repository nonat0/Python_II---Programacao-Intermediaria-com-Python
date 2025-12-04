from rich.console import Console
from rich.text import Text

console = Console()

def texto_colorido(texto: str, isArquivo: bool):
    """Mostra o texto colorido com fundo branco."""
    if isArquivo:
        with open(texto, "r", encoding="utf-8") as f:
            texto = f.read()
    t = Text(texto, style="bold red on white")
    console.print(t)

def texto_sublinhado(texto: str, isArquivo: bool):
    """Mostra o texto sublinhado."""
    if isArquivo:
        with open(texto, "r", encoding="utf-8") as f:
            texto = f.read()
    t = Text(texto, style="underline")
    console.print(t)
