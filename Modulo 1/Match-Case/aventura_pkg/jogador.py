import tkinter as tk
from tkinter import messagebox
from typing import List, Tuple
from aventura_pkg import utils, labirinto
import time
CELL_SIZE = 18  # base pixels per cell; will scale if needed

class GameWindow:
    """
    Classe responsável pela janela principal do jogo e toda a lógica de renderização
    e interação com o jogador.
    """
    
    def __init__(self, root, lab: List[List[str]], apple_pos: Tuple[int,int], 
                 victory_sound="victory.wav", player_color="#40a9ff"):
        """
        Inicializa a janela do jogo com o labirinto e configurações.
        
        Args:
            root (tk.Tk): Janela raiz do Tkinter.
            lab (List[List[str]]): Matriz representando o labirinto.
            apple_pos (Tuple[int,int]): Posição (linha, coluna) da maçã.
            victory_sound (str): Caminho para o arquivo de som de vitória.
            player_color (str): Código hexadecimal da cor da bolinha do jogador.
        """
        self.lab = lab
        self.apple_pos = apple_pos
        self.rows = len(lab)
        self.cols = len(lab[0])
        self.root = root
        self.player_color = player_color  # Armazena a cor personalizada
        
        self.window = tk.Toplevel(root)
        self.window.title("Aventura no Labirinto")
        
        # Calcula dimensões do canvas
        canvas_width = self.cols * CELL_SIZE
        canvas_height = self.rows * CELL_SIZE
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        
        # Ajusta escala se necessário para caber na tela
        if canvas_width > screen_w - 120:
            scale = (screen_w - 120)/canvas_width
        else:
            scale = 1.0
        self.cell_size = max(8, int(CELL_SIZE * scale))
        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size

        self.canvas = tk.Canvas(self.window, width=canvas_width, height=canvas_height, bg="black")
        self.canvas.pack()

        # Frame de status (tempo e movimentos)
        self.status = tk.Frame(self.window)
        self.status.pack(fill='x')
        self.moves = 0
        self.start_time = time.time()
        self.time_label = tk.Label(self.status, text="Tempo: 0.0s")
        self.moves_label = tk.Label(self.status, text="Movimentos: 0")
        self.time_label.pack(side='left', padx=10, pady=4)
        self.moves_label.pack(side='right', padx=10, pady=4)

        # Posição inicial do jogador
        self.player = [1, 1]
        if self.lab[self.player[0]][self.player[1]] == '#':
            # Procura primeiro espaço vazio se posição inicial estiver bloqueada
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.lab[r][c] == ' ':
                        self.player = [r, c]
                        break
                else:
                    continue
                break

        self.victory_sound = victory_sound
        self.draw_labirinto()
        self.window.bind("<Key>", self.on_key)
        self.window.focus_force()
        self._running = True
        self.update_timer()

    def draw_labirinto(self):
        """
        Renderiza o labirinto completo no canvas, incluindo paredes, espaços vazios,
        a maçã e o jogador com sua cor personalizada.
        """
        self.canvas.delete("all")
        
        # Desenha todas as células do labirinto
        for r in range(self.rows):
            for c in range(self.cols):
                x0 = c * self.cell_size
                y0 = r * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                val = self.lab[r][c]
                
                if val == '#':
                    # Parede
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#222222", outline="#111111")
                elif val == ' ':
                    # Espaço vazio
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#f5f5f5", outline="#e0e0e0")
                elif val == '🍎':
                    # Maçã (objetivo)
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="#a8e6a1", outline="#79c06a")
                    try:
                        self.canvas.create_text(
                            x0 + self.cell_size/2, 
                            y0 + self.cell_size/2, 
                            text='🍎', 
                            font=("Segoe UI Emoji", int(self.cell_size*0.8))
                        )
                    except Exception:
                        # Fallback se emoji não funcionar
                        self.canvas.create_oval(x0+4, y0+4, x1-4, y1-4, fill="red")
        
        # Desenha o jogador (bolinha) com a cor personalizada
        pr, pc = self.player
        x0 = pc * self.cell_size
        y0 = pr * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        
        # Calcula cor de borda mais escura
        outline_color = self._darken_color(self.player_color)
        
        self.canvas.create_oval(
            x0+3, y0+3, x1-3, y1-3, 
            fill=self.player_color, 
            outline=outline_color, 
            width=2,
            tags="player"
        )

    def _darken_color(self, hex_color):
        """
        Escurece uma cor hexadecimal para criar uma borda mais escura.
        
        Args:
            hex_color (str): Cor em formato hexadecimal (#RRGGBB).
            
        Retorna:
            str: Cor escurecida em formato hexadecimal.
        """
        # Remove o '#' e converte para RGB
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Escurece cada componente em 40%
        r = int(r * 0.6)
        g = int(g * 0.6)
        b = int(b * 0.6)
        
        return f'#{r:02x}{g:02x}{b:02x}'

    def update_timer(self):
        """
        Atualiza o cronômetro exibido na interface a cada 100ms.
        Continua executando enquanto o jogo estiver ativo.
        """
        if not self._running:
            return
        elapsed = time.time() - self.start_time
        self.time_label.config(text=f"Tempo: {elapsed:.1f}s")
        self.window.after(100, self.update_timer)

    def on_key(self, event):
        """
        Processa eventos de teclado para movimentação do jogador.
        
        Args:
            event (tk.Event): Evento de pressionamento de tecla.
        """
        key = event.keysym.lower()
        
        # Mapeia teclas para direções de movimento
        move_map = {
            'w': (-1, 0), 'up': (-1, 0),      # Cima
            's': (1, 0), 'down': (1, 0),       # Baixo
            'a': (0, -1), 'left': (0, -1),     # Esquerda
            'd': (0, 1), 'right': (0, 1),      # Direita
            'q': 'quit'                         # Sair
        }
        
        if key not in move_map:
            return
        
        delta = move_map[key]
        
        # Comando de sair
        if delta == 'quit':
            self._running = False
            self.window.destroy()
            return
        
        # Calcula nova posição
        dr, dc = delta
        nr = self.player[0] + dr
        nc = self.player[1] + dc
        
        # Verifica se movimento é válido (dentro dos limites e não é parede)
        if 0 <= nr < self.rows and 0 <= nc < self.cols and self.lab[nr][nc] != '#':
            self.player = [nr, nc]
            self.moves += 1
            self.moves_label.config(text=f"Movimentos: {self.moves}")
            self.draw_labirinto()
            
            # Verifica se chegou na maçã (vitória)
            if (nr, nc) == self.apple_pos:
                elapsed = time.time() - self.start_time
                self._running = False
                utils.play_victory_sound(self.victory_sound)
                utils.tela_vitoria_gui(self.window, winner="Você", time_seconds=elapsed, moves=self.moves)