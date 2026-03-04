from datetime import datetime
from sqlalchemy import select
from app import db
from app.models.models import User, Post

def validate_user_password(username, password):
    """
    Valida credenciais de login do usuário.
    
    Args:
        username (str): Nome de usuário
        password (str): Senha em texto plano
        
    Returns:
        User | None: Objeto User se válido, None caso contrário
    """
    res = db.session.scalars(select(User).where(User.username == username))
    user = res.first()
    
    if user and user.check_password(password):
        return user
    else:
        return None

def user_exists(username):
    """
    Verifica se usuário já existe no banco.
    
    Args:
        username (str): Nome de usuário para verificação
        
    Returns:
        User | None: Objeto User se encontrado
    """
    res = db.session.scalars(select(User).where(User.username == username))
    user = res.first()
    return user

def create_user(username, password, remember=False, photo_url=None, bio=None, last_login=None):
    """
    Cria novo usuário com perfil completo.
    
    Args:
        username (str): Nome de usuário único
        password (str): Senha em texto plano (será hasheada)
        remember (bool, optional): Flag de persistência
        photo_url (str, optional): URL da foto de perfil
        bio (str, optional): Biografia do usuário
        last_login (datetime, optional): Data do último login
        
    Returns:
        User: Usuário recém-criado
    """
    new_user = User(
        username=username,
        remember=remember,
        photo_url=photo_url,
        bio=bio,
        last_login=last_login if last_login else datetime.now()
    )
    
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return new_user

def create_post(user_id, body):
    """
    Cria um novo post associado a um usuário.
    
    Args:
        user_id (int): ID do usuário autor
        body (str): Conteúdo textual do post
        
    Returns:
        Post: Post recém-criado
        
    Raises:
        ValueError: Se user_id não existir ou body estiver vazio
    """
    if not body or not body.strip():
        raise ValueError("O conteúdo do post não pode estar vazio")
    
    user = db.session.get(User, user_id)
    if not user:
        raise ValueError(f"Usuário com ID {user_id} não encontrado")
    
    new_post = Post(
        body=body.strip(),
        user_id=user_id,
        timestamp=datetime.utcnow()
    )
    
    db.session.add(new_post)
    db.session.commit()
    
    return new_post

def get_timeline(limit=5):
    """
    Retorna os posts mais recentes de todos os usuários.
    
    Utiliza o relacionamento 'author' do Post para acessar dados do usuário
    sem necessidade de JOIN manual.
    
    Args:
        limit (int, optional): Número máximo de posts a retornar. Padrão: 5
        
    Returns:
        list[Post]: Lista dos posts mais recentes
        
    Example:
        >>> posts = get_timeline(5)
        >>> for post in posts:
        ...     print(f'{post.author.username}: {post.body}')
    """
    posts = db.session.scalars(
        select(Post)
        .order_by(Post.timestamp.desc())
        .limit(limit)
    ).all()
    
    return posts

def get_user_posts(user_id):
    """
    Retorna todos os posts de um usuário específico.
    
    Args:
        user_id (int): ID do usuário
        
    Returns:
        list[Post]: Lista de posts ordenados por data (mais recentes primeiro)
    """
    posts = db.session.scalars(
        select(Post)
        .where(Post.user_id == user_id)
        .order_by(Post.timestamp.desc())
    ).all()
    
    return posts

def get_all_posts():
    """
    Retorna todos os posts do sistema.
    
    Returns:
        list[Post]: Lista de todos os posts ordenados por data
    """
    posts = db.session.scalars(
        select(Post)
        .order_by(Post.timestamp.desc())
    ).all()
    
    return posts

def update_post(post_id, new_body):
    """
    Atualiza o conteúdo de um post existente e registra data de edição.
    
    Automaticamente atualiza o campo edited_at para a data/hora atual.
    
    Args:
        post_id (int): ID do post a ser atualizado
        new_body (str): Novo conteúdo do post
        
    Returns:
        Post: Post atualizado
        
    Raises:
        ValueError: Se post não existir ou body estiver vazio
        
    Example:
        >>> post = update_post(1, 'Conteúdo atualizado')
        >>> print(post.edited_at)  # Mostra data da edição
    """
    if not new_body or not new_body.strip():
        raise ValueError("O conteúdo do post não pode estar vazio")
    
    post = db.session.get(Post, post_id)
    if not post:
        raise ValueError(f"Post com ID {post_id} não encontrado")
    
    post.body = new_body.strip()
    post.edited_at = datetime.now()  # Registra data da edição
    db.session.commit()
    
    return post

def delete_post(post_id):
    """
    Remove um post do banco de dados.
    
    Args:
        post_id (int): ID do post a ser deletado
        
    Returns:
        bool: True se deletado com sucesso
        
    Raises:
        ValueError: Se post não existir
    """
    post = db.session.get(Post, post_id)
    if not post:
        raise ValueError(f"Post com ID {post_id} não encontrado")
    
    db.session.delete(post)
    db.session.commit()
    
    return True