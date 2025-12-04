import sqlite3
import bcrypt
from datetime import datetime

DB_NAME = "pharmastock.db"

def init_db():
    """Inicializa o banco de dados e cria as tabelas necessárias."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Tabela de Usuários
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # Tabela de Medicamentos
    c.execute('''
        CREATE TABLE IF NOT EXISTS medicamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            lote TEXT NOT NULL,
            validade TEXT NOT NULL,
            fabricante TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            atualizado_em TEXT
        )
    ''')
    
    # Criar Admin padrão se não existir
    c.execute("SELECT * FROM usuarios WHERE username = 'admin'")
    if not c.fetchone():
        senha_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
        c.execute("INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)", 
                  ('admin', senha_hash, 'admin'))
        print("Usuário 'admin' criado com senha 'admin123'")
    
    conn.commit()
    conn.close()

# --- FUNÇÕES DE AUTENTICAÇÃO ---

def verificar_login(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT password, role FROM usuarios WHERE username = ?", (username,))
    data = c.fetchone()
    conn.close()
    
    if data:
        stored_password, role = data
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return role
    return None

def criar_usuario(username, password, role='user'):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        senha_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        c.execute("INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)", 
                  (username, senha_hash, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Usuário já existe
    finally:
        conn.close()

# --- FUNÇÕES DE ESTOQUE ---

def cadastrar_medicamento(dados):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    dados['atualizado_em'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO medicamentos (nome, lote, validade, fabricante, quantidade, atualizado_em)
        VALUES (:nome, :lote, :validade, :fabricante, :quantidade, :atualizado_em)
    ''', dados)
    conn.commit()
    conn.close()

def listar_medicamentos():
    conn = sqlite3.connect(DB_NAME)
    # Retorna dicionários em vez de tuplas
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    c.execute("SELECT * FROM medicamentos")
    items = [dict(row) for row in c.fetchall()]
    conn.close()
    return items

def atualizar_quantidade(id_med, nova_qtd):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE medicamentos SET quantidade = ?, atualizado_em = ? WHERE id = ?", 
              (nova_qtd, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id_med))
    conn.commit()
    conn.close()

def excluir_medicamento(id_med):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM medicamentos WHERE id = ?", (id_med,))
    conn.commit()
    conn.close()