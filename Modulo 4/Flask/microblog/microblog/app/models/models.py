from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional

class User(UserMixin, db.Model):
    """
    Modelo de usuário com perfil completo.
    
    Inclui autenticação segura, foto de perfil e biografia.
    
    Attributes:
        id (int): Identificador único
        username (str): Nome de usuário único
        password_hash (str): Hash da senha
        remember (bool): Flag para persistência de sessão
        last_login (datetime): Último acesso
        photo_url (str, optional): URL da foto de perfil
        bio (str, optional): Biografia do usuário
        posts (relationship): Relação com posts do usuário
    """
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    remember: Mapped[bool] = mapped_column(default=False)
    last_login: Mapped[datetime] = mapped_column()
    
    # ✅ NOVOS CAMPOS
    photo_url: Mapped[Optional[str]] = mapped_column(default=None, nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(default=None, nullable=True)
    
    # Relacionamento com posts
    posts: Mapped[list["Post"]] = relationship('Post', back_populates='author', lazy='dynamic')

    def set_password(self, password):
        """
        Gera hash seguro da senha.
        
        Args:
            password (str): Senha em texto plano
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Valida senha fornecida contra o hash armazenado.
        
        Args:
            password (str): Senha para verificação
            
        Returns:
            bool: True se senha correta
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'User(id={self.id}, username={self.username})'


class Post(db.Model):
    """
    Modelo para posts de usuários com rastreamento de edições.
    
    Cada post está associado a um usuário através de chave estrangeira.
    Mantém registro da data de criação e da última edição.
    
    Attributes:
        id (int): Identificador único do post
        body (str): Conteúdo textual do post
        timestamp (datetime): Data e hora de criação
        edited_at (datetime, optional): Data e hora da última edição
        user_id (int): ID do usuário autor (FK)
        author (relationship): Relação com o usuário autor
    """
    __tablename__ = 'posts'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    body: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    edited_at: Mapped[Optional[datetime]] = mapped_column(default=None, nullable=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'), nullable=False)
    
    # Relacionamento com usuário
    author: Mapped["User"] = relationship('User', back_populates='posts')
    
    def __repr__(self) -> str:
        return f'Post(id={self.id}, body={self.body[:20]}..., author={self.author.username})'