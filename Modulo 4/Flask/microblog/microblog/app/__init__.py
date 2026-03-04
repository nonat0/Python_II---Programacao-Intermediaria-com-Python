import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

"""
Módulo de inicialização da aplicação Flask.

Este módulo configura:
- Instância do Flask com suporte a arquivos estáticos
- Conexão com banco de dados SQLite
- Flask-Login para gerenciamento de sessões
- Criação automática das tabelas do banco
"""

# Criando instância do Flask
app = Flask(__name__, 
            static_folder='static',  # Pasta para CSS, JS, imagens
            static_url_path='/static')

# Configurações da aplicação
app.config['SECRET_KEY'] = "pd123"  # Chave secreta para sessões e formulários
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///microblog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilita warnings

# Iniciando conexão com banco de dados SQLite
db = SQLAlchemy()
db.init_app(app)

# Configurando Flask-Login ANTES de importar os models
login = LoginManager(app)
login.login_view = 'login'  # Define a rota de login para redirecionamento
login.login_message = 'Por favor, faça login para acessar esta página.'
login.login_message_category = 'info'

# ✅ AGORA podemos importar models (que usa 'login')
from app.models import models

# ✅ Configurar o user_loader DEPOIS de importar User
@login.user_loader
def load_user(id):
    """
    Callback necessário para o Flask-Login recarregar o usuário da sessão.
    
    Args:
        id (str): ID do usuário armazenado na sessão
        
    Returns:
        User: Objeto do usuário ou None se não encontrado
    """
    return db.session.get(models.User, int(id))

# ✅ Importar routes e alquimias POR ÚLTIMO
from app import routes, alquimias

# Criando as tabelas no banco de dados
with app.app_context():
    db.create_all()