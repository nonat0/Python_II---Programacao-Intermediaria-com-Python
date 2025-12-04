from rich.panel import Panel
from rich.console import Console

console = Console()

def painel_padrao(texto: str, isArquivo: bool):
    """Exibe o texto dentro de um painel padrão."""
    if isArquivo:
        with open(texto, "r", encoding="utf-8") as f:
            texto = f.read()
    console.print(Panel(texto, title="Painel Padrão"))

def painel_estilizado(texto: str, isArquivo: bool):
    """Exibe o texto dentro de um painel colorido e estilizado."""
    if isArquivo:
        with open(texto, "r", encoding="utf-8") as f:
            texto = f.read()
    console.print(Panel(texto, title="[bold magenta]Painel Estilizado[/bold magenta]", border_style="bright_blue"))
