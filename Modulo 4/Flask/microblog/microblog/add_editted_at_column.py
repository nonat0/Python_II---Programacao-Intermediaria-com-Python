"""
Script de migração para adicionar coluna edited_at à tabela posts.

Execute este script UMA VEZ para atualizar o banco de dados existente.
Não é necessário recriar o banco ou perder dados.

Como usar:
    python add_edited_at_column.py
"""

from app import app, db
from sqlalchemy import text

def migrate_database():
    """
    Adiciona a coluna edited_at à tabela posts se ela não existir.
    
    Esta migração é segura e pode ser executada múltiplas vezes.
    Se a coluna já existir, não faz nada.
    """
    with app.app_context():
        try:
            # Verifica se a coluna já existe
            result = db.session.execute(text("PRAGMA table_info(posts)"))
            columns = [row[1] for row in result]
            
            if 'edited_at' in columns:
                print("✅ Coluna 'edited_at' já existe. Nenhuma ação necessária.")
                return
            
            # Adiciona a coluna edited_at
            print("🔄 Adicionando coluna 'edited_at' à tabela posts...")
            db.session.execute(text(
                "ALTER TABLE posts ADD COLUMN edited_at DATETIME"
            ))
            db.session.commit()
            print("✅ Coluna 'edited_at' adicionada com sucesso!")
            print("📝 Nota: Posts existentes terão edited_at = NULL (não editados)")
            
        except Exception as e:
            print(f"❌ Erro durante a migração: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Iniciando Migração do Banco de Dados")
    print("=" * 60)
    print()
    
    migrate_database()
    
    print()
    print("=" * 60)
    print("✨ Migração Concluída!")
    print("=" * 60)
    print()
    print("📌 Próximos passos:")
    print("   1. Reinicie o Flask: flask run")
    print("   2. Edite um post para testar")
    print("   3. Veja a data de edição aparecer!")
    print()