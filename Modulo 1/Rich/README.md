# Exercício - Biblioteca Rich

Exercício de uso da biblioteca [Rich](https://rich.readthedocs.io/).

## Requisitos
- Python 3.10+
- Biblioteca `rich`

## Instalação
`!/bin/bash`
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install rich

## Exemplo de Uso (Comandos):
```bash

# Painel personalizado com mensagem passada manualmente ou utilizando o parse '<arquivo.tipo> -a'
python main.py "Olá Mundo" -m painel -f painel_padrao 
python main.py "Olá Mundo" -m painel -f painel_estilizado

# Modificar estilo de texto
python main.py "texto.txt" -a -m estilo -f texto_colorido
python main.py "texto.txt" -a -m estilo -f texto_sublinhado

# Exibir animação de barra de progresso
python main.py "Processando dados..." -m progresso -f barra_progresso
python main.py "Processando dados..." -m progresso -f progresso_simples

# Exibe um layout com cabeçalho, conteúdo carregável via parser '<arquivo.tipo> -a' e um rodapé
python main.py "texto.txt"-a -m layout -f mostrar_layout
python main.py "texto.txt"-a -m layout -f layout_simples

```
