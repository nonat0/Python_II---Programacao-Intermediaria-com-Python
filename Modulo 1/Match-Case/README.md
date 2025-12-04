# Aventura no Labirinto 

Labirinto é gerado aleatoriamente a cada partida.
O objetivo é encontrar a 🍎. Use W/A/S/D ou as setas para mover. Pressione Q para sair.

## Funcionalidades 
- Labirinto aleatório (DFS recursive backtracker)
- Interface Tkinter com Canvas
- Cronômetro de tempo exibido ao final
- Contagem de movimentos
- Animação de vitória (recursiva com after)
- Argparse com personalização (Utilize os comandos da seção abaixo)

### Personalização com Argparse
```bash
Modo padrão (interativo)
python main.py

# Cor do player suporta: red, yellow, blue
   python main.py --color vermelho
   python main.py --color amarelo
   python main.py --color azul

# Dificuldade (tamanho do labirinto) suporta: easy, hard, medium
   python main.py --dificuldade facil
   python main.py --dificuldade medio
   python main.py --dificuldade dificil

# Extra: Comando Help personalizado:
 python main.py --help
```
### Bashs rápidos para copiar e colar:

```bash
# Tudo personalizado
python main.py --name "Labirinto argparse" --color red --dificuldade facil

# Jogo rápido no difícil com bolinha amarela
python main.py --color amarelo --dificuldade facil

# Ver ajuda
python main.py --help

```
## Como executar

1. Crie e ative um ambiente virtual (recomendado):
```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# Linux / macOS
source venv/bin/activate
```

2. Instale dependências:
```bash
pip install -r requirements.txt
```

3. Execute:
```bash
python main.py
```


