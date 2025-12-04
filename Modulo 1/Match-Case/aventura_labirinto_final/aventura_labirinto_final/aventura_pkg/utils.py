import tkinter as tk
import threading
import os
from pathlib import Path

def imprime_instrucoes():
    """
    Exibe uma janela com as instruções do jogo em formato texto.
    Utiliza um widget Text desabilitado para evitar edições.
    """
    texto = (
        "Instruções:\n\n"
        "- Use as teclas W/A/S/D ou as setas para se mover.\n"
        "- Encontre a 🍎 para vencer.\n"
        "- Pressione Q para sair durante o jogo.\n\n"
        "Dica: escolha dificuldade 'difícil' para labirintos maiores."
    )
    win = tk.Toplevel()
    win.title("Instruções")
    txt = tk.Text(win, width=60, height=12, wrap='word')
    txt.insert('1.0', texto)
    txt.config(state='disabled')
    txt.pack(padx=10, pady=10)
    btn = tk.Button(win, text="Fechar", command=win.destroy)
    btn.pack(pady=6)


def play_victory_sound(path="victory.wav"):
    """
    Toca um arquivo de som WAV em uma thread separada para não bloquear o jogo.
    Tenta múltiplas bibliotecas de áudio como fallback.
    
    Args:
        path (str): Caminho relativo ou absoluto para o arquivo WAV.
    """
    def _play():
        # Resolve o caminho absoluto do arquivo
        if not os.path.isabs(path):
            # Tenta primeiro na pasta atual
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Vai para o diretório pai (raiz do projeto)
            project_root = os.path.dirname(script_dir)
            full_path = os.path.join(project_root, path)
            
            # Se não encontrar, tenta na pasta do script
            if not os.path.exists(full_path):
                full_path = os.path.join(script_dir, path)
            
            # Se ainda não encontrar, tenta na pasta de execução atual
            if not os.path.exists(full_path):
                full_path = path
        else:
            full_path = path
        
        # Verifica se o arquivo existe
        if not os.path.exists(full_path):
            print(f"⚠️ Arquivo de som não encontrado: {full_path}")
            return
        
        # Tenta tocar com simpleaudio primeiro
        try:
            import simpleaudio as sa
            wave_obj = sa.WaveObject.from_wave_file(full_path)
            play_obj = wave_obj.play()
            play_obj.wait_done()
            return
        except ImportError:
            print("⚠️ simpleaudio não instalado. Tentando pygame...")
        except Exception as e:
            print(f"⚠️ Erro ao tocar com simpleaudio: {e}")
        
        # Fallback 1: pygame
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play()
            # Aguarda o som terminar
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()
            return
        except ImportError:
            print("⚠️ pygame não instalado. Tentando playsound...")
        except Exception as e:
            print(f"⚠️ Erro ao tocar com pygame: {e}")
        
        # Fallback 2: playsound
        try:
            from playsound import playsound
            playsound(full_path)
            return
        except ImportError:
            print("⚠️ playsound não instalado.")
        except Exception as e:
            print(f"⚠️ Erro ao tocar com playsound: {e}")
        
        # Fallback 3: winsound (apenas Windows)
        try:
            import winsound
            winsound.PlaySound(full_path, winsound.SND_FILENAME)
            return
        except ImportError:
            pass  # winsound só existe no Windows
        except Exception as e:
            print(f"⚠️ Erro ao tocar com winsound: {e}")
        
        print("❌ Nenhuma biblioteca de áudio disponível para tocar o som.")
        print("   Instale uma das seguintes: simpleaudio, pygame ou playsound")
    
    # Executa em thread separada para não bloquear a interface
    t = threading.Thread(target=_play, daemon=True)
    t.start()


def tela_vitoria_gui(root, winner="Jogador", time_seconds=0.0, moves=0):
    """
    Exibe uma janela de vitória animada com informações da partida.
    Utiliza função recursiva interna para criar animação de estrelas.
    
    Args:
        root (tk.Tk ou tk.Toplevel): Janela pai.
        winner (str): Nome do vencedor a ser exibido.
        time_seconds (float): Tempo total da partida em segundos.
        moves (int): Número total de movimentos realizados.
    """
    win = tk.Toplevel(root)
    win.title("Vitória!")
    
    # Título principal
    lbl = tk.Label(
        win, 
        text=f"🎉 {winner}, você encontrou a maçã! 🎎", 
        font=("Segoe UI", 14, "bold")
    )
    lbl.pack(padx=20, pady=8)
    
    # Informações de desempenho
    info = tk.Label(
        win, 
        text=f"Tempo: {time_seconds:.2f} segundos\nMovimentos: {moves}", 
        font=("Segoe UI", 11)
    )
    info.pack(pady=6)
    
    def anim(count=0):
        """
        Função recursiva que cria animação de estrelas incrementais.
        A cada chamada adiciona mais estrelas até o limite.
        
        Args:
            count (int): Contador de iterações da animação (0 a 6).
        """
        if count > 6:
            # Quando termina a animação, exibe mensagem final
            footer = tk.Label(
                win, 
                text=f"Sua aventura terminou com sucesso!", 
                font=("Segoe UI", 11)
            )
            footer.pack(pady=6)
            return
        
        # Cria label com estrelas proporcionais ao contador
        star = tk.Label(win, text="✨" * ((count % 4) + 1), font=("Segoe UI", 16))
        star.pack()
        
        # Agenda próxima chamada recursiva após 250ms
        win.after(250, lambda: anim(count+1))
    
    # Inicia a animação recursiva
    anim()
    
    # Botão de fechar
    btn = tk.Button(
        win, 
        text="Fechar", 
        command=lambda: (win.destroy(), root.destroy())
    )
    btn.pack(pady=8)