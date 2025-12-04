from rich.progress import Progress
import time

def barra_progresso(texto: str, isArquivo: bool):
    """Exibe uma barra de progresso simulando uma tarefa e mostra o texto ao final."""
    if isArquivo:
        with open(texto, "r", encoding="utf-8") as f:
            texto = f.read()

    with Progress() as progress:
        tarefa = progress.add_task("Processando...", total=1000)
        while not progress.finished:
            progress.update(tarefa, advance=20)
            time.sleep(0.1)

    print(texto)

def progresso_simples(texto: str, isArquivo: bool):
    """Exibe uma barra de progresso rápida."""
    with Progress() as progress:
        tarefa = progress.add_task("Carregando...", total=5)
        for _ in range(5):
            time.sleep(0.2)
            progress.advance(tarefa)
