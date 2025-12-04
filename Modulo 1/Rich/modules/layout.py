from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from datetime import datetime

console = Console()

def mostrar_layout(texto: str, isArquivo: bool):
    """Exibe um layout completo com topo, conteúdo e rodapé."""
    if isArquivo:
        with open(texto, "r", encoding="utf-8") as f:
            texto = f.read()

    # Criar estrutura principal
    layout = Layout(name="root")
    layout.split_column(
        Layout(name="topo", size=3),
        Layout(name="conteudo", ratio=2),
        Layout(name="rodape", size=3)
    )

    hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    layout["topo"].update(
        Panel(
            f"[bold cyan]💡 Rich Layout Demo[/bold cyan]\n[green]Hora atual:[/green] {hora_atual}",
            title="[bold blue]TOPO[/bold blue]",
            border_style="bright_blue"
        )
    )

    layout["conteudo"].update(
        Panel(
            texto,
            title="[bold magenta]CONTEÚDO[/bold magenta]",
            border_style="magenta",
            padding=(1, 4)
        )
    )

    layout["rodape"].update(
        Panel(
            "[bold yellow]Feito com a biblioteca Rich 🤖[/bold yellow]",
            title="[bold green]RODAPÉ[/bold green]",
            border_style="yellow"
        )
    )

    console.print(layout)


def layout_simples(texto: str, isArquivo: bool):
    """Versão reduzida — mostra apenas o conteúdo centralizado."""
    if isArquivo:
        with open(texto, "r", encoding="utf-8") as f:
            texto = f.read()

    layout = Layout(name="root")
    layout.update(Panel(texto, title="Layout Simples", border_style="green"))
    console.print(layout)
