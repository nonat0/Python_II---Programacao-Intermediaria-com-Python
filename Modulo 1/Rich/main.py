import argparse
from modules import estilo, painel, progresso
from modules import layout

modulos = {
    "layout": layout,
    "painel": painel,
    "progresso": progresso,
    "estilo": estilo
}

def main():
    """Interface de linha de comando para o pacote modules."""
    parser = argparse.ArgumentParser(
        description="Interface para o pacote 'modules' usando Rich."
    )

    parser.add_argument(
        "texto",
        help="Texto ou caminho para o arquivo a ser exibido."
    )
    parser.add_argument(
        "-a", "--arquivo",
        action="store_true",
        help="Indica que o texto é o caminho de um arquivo."
    )
    parser.add_argument(
        "-m", "--modulo",
        choices=modulos.keys(),
        required=True,
        help="Escolhe o módulo a ser usado."
    )
    parser.add_argument(
        "-f", "--funcao",
        required=True,
        help="Escolhe a função do módulo a ser usada."
    )

    args = parser.parse_args()

    modulo = modulos[args.modulo]
    try:
        funcao = getattr(modulo, args.funcao)
    except AttributeError:
        print(f"Função '{args.funcao}' não encontrada no módulo '{args.modulo}'.")
        return

    funcao(args.texto, args.arquivo)

if __name__ == "__main__":
    main()