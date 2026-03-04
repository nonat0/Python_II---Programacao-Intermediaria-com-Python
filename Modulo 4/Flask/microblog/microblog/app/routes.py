from flask import (
    render_template,
    request,
    url_for,
    redirect,
    flash
)
from app import app, db
from app import alquimias
from flask_login import login_user, logout_user, current_user, login_required

"""
Rotas da aplicação Microblog.

Inclui autenticação, CRUD de posts e gerenciamento de perfil.
"""

@app.route('/')
@login_required
def index():
    """
    Página inicial (home) com timeline de posts.
    
    Exibe os 5 posts mais recentes de todos os usuários usando get_timeline().
    Requer autenticação (redireciona para login se não autenticado).
    """
    user = None
    posts = []
    
    if current_user.is_authenticated:
        user = current_user
        posts = alquimias.get_timeline(limit=5)

    return render_template(
        'index.html',
        title='Home',
        user=user,
        posts=posts
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota de login (GET: exibe formulário, POST: processa login).
    
    Se já autenticado, redireciona para index.
    Valida credenciais e inicia sessão se válidas.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        
        user = alquimias.validate_user_password(username, password)
        
        if user: 
            print("Login bem-sucedido")
            login_user(user, remember=user.remember)
            return redirect(url_for('index'))
        else:
            print("Usuário ou senha inválidos")
            flash('Usuário ou senha inválidos', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html', title='Sign In')

@app.route('/cadastro', methods=['GET', 'POST'])
def register():
    """
    Rota de cadastro de novo usuário.
    
    GET: Exibe formulário de cadastro com campos de perfil.
    POST: Cria novo usuário com foto e bio, depois faz login automático.
    """
    if request.method == 'GET':
        return render_template('cadastro.html', title='Cadastro')
    
    username = request.form['username'].lower()
    
    if alquimias.user_exists(username):
        print("\n Username already taken \n")
        flash('Nome de usuário já está em uso', 'error')
        return redirect(url_for('register'))
    
    password = request.form['password']
    remember = True if request.form.get('remember') == 'on' else False
    photo_url = request.form.get('photo_url', '').strip() or None
    bio = request.form.get('bio', '').strip() or None
    
    user = alquimias.create_user(
        username=username,
        password=password,
        remember=remember,
        photo_url=photo_url,
        bio=bio
    )
    
    login_user(user, remember=remember)
    flash(f'Bem-vindo, {user.username}!', 'success')
    
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    """
    Encerra sessão do usuário e redireciona para login.
    """
    logout_user()
    return redirect(url_for('login'))

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    """
    Rota para criação de posts.
    
    GET: Renderiza formulário post.html para criar novo post.
    POST: Processa dados do formulário, cria post e redireciona para index.
    
    Requer autenticação (@login_required).
    """
    if request.method == 'GET':
        return render_template('post.html', title='Criar Post')
    
    body = request.form.get('body', '').strip()
    
    if not body:
        flash('O post não pode estar vazio', 'error')
        return redirect(url_for('post'))
    
    try:
        alquimias.create_post(user_id=current_user.id, body=body)
        flash('Post criado com sucesso!', 'success')
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('post'))
    
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """
    Edita um post existente.
    
    Apenas o autor do post pode editá-lo.
    
    Args:
        post_id (int): ID do post a ser editado
    """
    from app.models.models import Post
    post = Post.query.get_or_404(post_id)
    
    if post.user_id != current_user.id:
        flash('Você não tem permissão para editar este post', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        return render_template('edit_post.html', title='Editar Post', post=post)
    
    new_body = request.form.get('body', '').strip()
    
    try:
        alquimias.update_post(post_id, new_body)
        flash('Post atualizado com sucesso!', 'success')
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('edit_post', post_id=post_id))
    
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """
    Deleta um post existente.
    
    Apenas o autor do post pode deletá-lo.
    
    Args:
        post_id (int): ID do post a ser deletado
    """
    from app.models.models import Post
    post = Post.query.get_or_404(post_id)
    
    if post.user_id != current_user.id:
        flash('Você não tem permissão para deletar este post', 'error')
        return redirect(url_for('index'))
    
    try:
        alquimias.delete_post(post_id)
        flash('Post deletado com sucesso!', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('index'))

@app.route('/profile/photo', methods=['GET', 'POST'])
@login_required
def update_photo():
    """
    Atualiza ou remove a foto de perfil do usuário.
    
    GET: Renderiza formulário de edição de foto com preview.
    POST: Processa URL da nova foto ou remoção.
    
    Actions:
        - update: Atualiza photo_url com nova URL
        - remove: Remove foto (volta para user.png padrão)
    """
    if request.method == 'GET':
        return render_template('edit_photo.html', title='Editar Foto', user=current_user)
    
    action = request.form.get('action')
    
    if action == 'remove':
        current_user.photo_url = None
        db.session.commit()
        flash('Foto de perfil removida com sucesso!', 'success')
    else:
        photo_url = request.form.get('photo_url', '').strip()
        if photo_url:
            current_user.photo_url = photo_url
            db.session.commit()
            flash('Foto de perfil atualizada com sucesso!', 'success')
        else:
            flash('Por favor, forneça uma URL válida', 'error')
    
    return redirect(url_for('index'))

@app.route('/profile/bio', methods=['GET', 'POST'])
@login_required
def update_bio():
    """
    Atualiza ou remove a bio do usuário.
    
    GET: Renderiza formulário de edição de bio com textarea preenchida.
    POST: Processa nova bio ou remoção.
    
    Actions:
        - update: Atualiza bio com novo texto
        - remove: Remove bio (campo fica NULL)
    """
    if request.method == 'GET':
        return render_template('edit_bio.html', title='Editar Bio', user=current_user)
    
    action = request.form.get('action')
    
    if action == 'remove':
        current_user.bio = None
        db.session.commit()
        flash('Bio removida com sucesso!', 'success')
    else:
        bio = request.form.get('bio', '').strip()
        if bio:
            current_user.bio = bio
            db.session.commit()
            flash('Bio atualizada com sucesso!', 'success')
        else:
            flash('Por favor, escreva algo na bio', 'error')
    
    return redirect(url_for('index'))