import sqlite3
import os

# Define o caminho absoluto baseado no diretório atual do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Local do arquivo database.py
PROJECT_DIR = os.path.dirname(BASE_DIR)  # Volta para o diretório do projeto
DATABASE_DIR = os.path.join(PROJECT_DIR, "database")
os.makedirs(DATABASE_DIR, exist_ok=True)  # Garante que a pasta existe

# Caminho completo do banco de dados
DB_PATH = os.path.join(DATABASE_DIR, "produtos.db")

def criar_tabelas():
    """Cria as tabelas necessárias no banco de dados."""
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            descricao TEXT NOT NULL,
            preco REAL NOT NULL,
            imagem TEXT
        )
    ''')
    
    conexao.commit()
    conexao.close()

def adicionar_produto(codigo, descricao, preco, imagem):
    """Adiciona um produto ao banco de dados."""
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO produtos (codigo, descricao, preco, imagem)
            VALUES (?, ?, ?, ?)
        ''', (codigo, descricao, preco, imagem))
        conexao.commit()
    except sqlite3.IntegrityError:
        print("Erro: Código já existe.")
    
    conexao.close()

def buscar_produto(codigo):
    """Busca um produto pelo código."""
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    
    cursor.execute('SELECT * FROM produtos WHERE codigo = ?', (codigo,))
    produto = cursor.fetchone()
    conexao.close()
    return produto
