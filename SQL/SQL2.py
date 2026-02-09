""" 
Script modular para operações básicas (CRUD) em banco de dados local, utilizando boas práticas como Context Managers e Row Factory. 
"""



import sqlite3
from contextlib import closing

DATABASE = "users.db"

def get_connection():
    """Cria a conexão e configura para retornar dicionários."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
    return conn

def init_db():
    """Cria a tabela inicial se não existir."""
    with get_connection() as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            """)
            conn.commit()

def insert_user(name, email):
    """Insere um novo usuário com tratamento de erro."""
    try:
        with get_connection() as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (?, ?)",
                    (name, email)
                )
                conn.commit()
                print(f"✅ Usuário {name} inserido com sucesso!")
    except sqlite3.IntegrityError:
        print(f"❌ Erro: O e-mail '{email}' já está em uso.")
    except sqlite3.Error as e:
        print(f"❌ Erro no banco de dados: {e}")

def list_users():
    """Retorna a lista de usuários cadastrados."""
    with get_connection() as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()

def delete_user(user_id):
    """Remove um usuário pelo ID."""
    with get_connection() as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            print(f"🗑️ Usuário ID {user_id} removido.")

# --- Execução Principal ---
if __name__ == "__main__":
    init_db()

    # Testando inserções
    insert_user("Roberta", "roberta@email.com")
    insert_user("Ana", "ana@email.com")
    
    # Listando de forma limpa
    print("\n--- Lista de Usuários ---")
    users = list_users()
    for user in users:
        # Agora você usa o nome da coluna! Muito mais legível:
        print(f"ID: {user['id']} | Nome: {user['name']} | E-mail: {user['email']}")