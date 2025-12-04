import tkinter as tk
from tkinter import simpledialog
from aventura_pkg.labirinto import gerar_labirinto
from aventura_pkg.jogador import GameWindow
from aventura_pkg.utils import imprime_instrucoes
import argparse
import sys

def criar_parser():
    """
    Cria e configura o parser de argumentos de linha de comando.
    
    Retorna:
        ArgumentParser: Parser configurado com todos os argumentos suportados.
    """
    parser = argparse.ArgumentParser(
        prog="Aventura no Labirinto",
        description="🎮 Jogo de aventura em labirinto com interface gráfica Tkinter",
        epilog="Exemplo: python main.py --name Rafael --color vermelho --dificuldade facil",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False  # Vamos personalizar o help
    )
    
    parser.add_argument(
        '--name',
        type=str,
        default="Aventura no Labirinto",
        metavar='<NOME>',
        help='Nome da janela do jogo (ex: --name "Rafael")'
    )
    
    parser.add_argument(
        '--color',
        type=str,
        default="azul",
        choices=['vermelho', 'red', 'amarelo', 'yellow', 'azul', 'blue'],
        metavar='<COR>',
        help='Cor da bolinha do jogador: vermelho/red, amarelo/yellow, azul/blue (padrão: azul)'
    )
    
    parser.add_argument(
        '--dificuldade',
        type=str,
        default=None,
        choices=['facil', 'fácil', 'easy', 'medio', 'médio', 'medium', 'dificil', 'difícil', 'hard'],
        metavar='<NIVEL>',
        help='Dificuldade do jogo: facil, medio, dificil (se não especificado, pergunta no início)'
    )
    
    parser.add_argument(
        '--help', '-h',
        action='store_true',
        help='Mostra esta mensagem de ajuda personalizada'
    )
    
    return parser


def mostrar_ajuda_personalizada():
    """
    Exibe uma interface gráfica personalizada com as instruções de uso do programa.
    """
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    
    win = tk.Toplevel()
    win.title("🎮 Ajuda - Aventura no Labirinto")
    win.geometry("650x480")
    win.configure(bg="#f0f0f0")
    
    # Título
    titulo = tk.Label(
        win, 
        text="🎮 Aventura no Labirinto - Ajuda",
        font=("Segoe UI", 16, "bold"),
        bg="#f0f0f0",
        fg="#333333"
    )
    titulo.pack(pady=15)
    
    # Frame para o texto
    frame_texto = tk.Frame(win, bg="white", relief="solid", borderwidth=1)
    frame_texto.pack(padx=20, pady=10, fill="both", expand=True)
    
    # Scrollbar
    scrollbar = tk.Scrollbar(frame_texto)
    scrollbar.pack(side="right", fill="y")
    
    # Text widget
    texto = tk.Text(
        frame_texto,
        wrap="word",
        font=("Consolas", 10),
        bg="white",
        fg="#222222",
        padx=15,
        pady=15,
        yscrollcommand=scrollbar.set
    )
    texto.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=texto.yview)
    
    # Conteúdo da ajuda
    ajuda_texto = """
📋 USO:
    python main.py [OPÇÕES]

🎨 OPÇÕES DISPONÍVEIS:

  --name <NOME>
      Nomeia a janela do jogo com o nome especificado.
      Exemplo: --name Rafael
      
  --color <COR>
      Define a cor da bolinha do jogador.
      Cores disponíveis: vermelho, red, amarelo, yellow, azul, blue
      Padrão: azul
      Exemplo: --color vermelho
      
  --dificuldade <NIVEL>
      Inicia o jogo com a dificuldade especificada.
      Níveis: facil, medio, dificil (aceita com ou sem acento)
      Se não especificado, será perguntado no início do jogo.
      Exemplo: --dificuldade facil
      
  --help, -h
      Mostra esta mensagem de ajuda.

📝 EXEMPLOS DE USO:

  # Jogo padrão (modo interativo)
  python main.py
  
  # Jogo com nome personalizado
  python main.py --name "Labirinto do Rafael"
  
  # Bolinha vermelha no modo fácil
  python main.py --color vermelho --dificuldade facil
  
  # Tudo personalizado
  python main.py --name "Desafio Extremo" --color amarelo --dificuldade dificil

🎮 CONTROLES NO JOGO:
  • W, ↑       - Mover para cima
  • S, ↓       - Mover para baixo
  • A, ←       - Mover para esquerda
  • D, →       - Mover para direita
  • Q          - Sair do jogo

🎯 OBJETIVO:
  Encontre a maçã 🍎 no labirinto!

📊 DIFICULDADES:
  • Fácil:     Labirinto 21x21
  • Médio:     Labirinto 31x31
  • Difícil:   Labirinto 41x41

💡 DICAS:
  • Use a dificuldade fácil para se familiarizar com o jogo
  • O cronômetro começa assim que o jogo inicia
  • Tente completar com o menor número de movimentos!
"""
    
    texto.insert("1.0", ajuda_texto)
    texto.config(state="disabled")
    
    # Botão fechar
    btn_fechar = tk.Button(
        win,
        text="Fechar",
        font=("Segoe UI", 11),
        bg="#4CAF50",
        fg="white",
        activebackground="#45a049",
        width=15,
        command=lambda: (win.destroy(), root.destroy())
    )
    btn_fechar.pack(pady=15)
    
    win.mainloop()


def normalizar_cor(cor_input):
    """
    Converte o nome da cor em inglês ou português para o código hexadecimal.
    
    Args:
        cor_input (str): Nome da cor fornecida pelo usuário.
        
    Retorna:
        str: Código hexadecimal da cor correspondente.
    """
    mapa_cores = {
        'vermelho': '#FF4444',
        'red': '#FF4444',
        'amarelo': '#FFD700',
        'yellow': '#FFD700',
        'azul': '#40a9ff',
        'blue': '#40a9ff'
    }
    return mapa_cores.get(cor_input.lower(), '#40a9ff')


def escolher_dificuldade():
    """
    Abre um diálogo para o usuário escolher a dificuldade do jogo.
    
    Retorna:
        str: Dificuldade escolhida (normalizada em minúsculas).
    """
    choice = simpledialog.askstring(
        "Dificuldade", 
        "Escolha dificuldade: fácil, médio, difícil", 
        initialvalue="fácil"
    )
    if not choice:
        return "fácil"
    return choice.lower().strip()


def obter_tamanho_labirinto(dificuldade):
    """
    Determina o tamanho do labirinto baseado na dificuldade escolhida.
    
    Args:
        dificuldade (str): Nível de dificuldade do jogo.
        
    Retorna:
        int: Tamanho do labirinto (sempre ímpar).
    """
    match dificuldade.lower():
        case "fácil" | "facil" | "easy":
            return 21
        case "médio" | "medio" | "medium":
            return 31
        case "difícil" | "dificil" | "hard":
            return 41
        case _:
            return 31


def iniciar_jogo(root, dificuldade_preset=None, cor_jogador="#40a9ff"):
    """
    Inicia uma nova partida do jogo com as configurações especificadas.
    
    Args:
        root (tk.Tk): Janela principal do Tkinter.
        dificuldade_preset (str, optional): Dificuldade pré-definida via CLI.
        cor_jogador (str): Código hexadecimal da cor da bolinha do jogador.
    """
    if dificuldade_preset:
        dificuldade = dificuldade_preset
    else:
        dificuldade = escolher_dificuldade()
    
    tamanho = obter_tamanho_labirinto(dificuldade)
    lab, apple_pos = gerar_labirinto(tamanho, tamanho)
    GameWindow(root, lab, apple_pos, victory_sound="victory.wav", player_color=cor_jogador)


def criar_menu(nome_janela="Aventura no Labirinto", dificuldade_preset=None, cor_jogador="#40a9ff"):
    """
    Cria e exibe o menu principal do jogo.
    
    Args:
        nome_janela (str): Título da janela principal.
        dificuldade_preset (str, optional): Dificuldade pré-configurada.
        cor_jogador (str): Cor da bolinha do jogador em hexadecimal.
    """
    root = tk.Tk()
    root.title(nome_janela)
    root.geometry("420x280")
    
    lbl = tk.Label(root, text="Aventura no Labirinto", font=("Segoe UI", 18, "bold"))
    lbl.pack(pady=12)

    btn_play = tk.Button(
        root, 
        text="Jogar", 
        width=24, 
        command=lambda: iniciar_jogo(root, dificuldade_preset, cor_jogador)
    )
    btn_instru = tk.Button(root, text="Instruções", width=24, command=imprime_instrucoes)
    btn_sair = tk.Button(root, text="Sair", width=24, command=root.destroy)

    btn_play.pack(pady=10)
    btn_instru.pack(pady=6)
    btn_sair.pack(pady=6)

    root.mainloop()


if __name__ == "__main__":
    parser = criar_parser()
    
    # Se --help foi passado, mostra ajuda personalizada
    if '--help' in sys.argv or '-h' in sys.argv:
        mostrar_ajuda_personalizada()
        sys.exit(0)
    
    args = parser.parse_args()
    
    # Normaliza a cor escolhida
    cor_jogador = normalizar_cor(args.color)
    
    # Inicia o menu com as configurações
    criar_menu(
        nome_janela=args.name,
        dificuldade_preset=args.dificuldade,
        cor_jogador=cor_jogador
    )