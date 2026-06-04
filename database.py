import sqlite3
import os
# pyrefly: ignore [missing-import]
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stockmaster.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            nome    TEXT NOT NULL,
            email   TEXT UNIQUE NOT NULL,
            senha   TEXT NOT NULL,
            perfil  TEXT NOT NULL DEFAULT 'vendedor'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fornecedores (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            nome    TEXT NOT NULL,
            contato TEXT,
            cnpj    TEXT UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nome            TEXT NOT NULL,
            categoria       TEXT,
            descricao       TEXT,
            unidade         TEXT NOT NULL DEFAULT 'un',
            quantidade      REAL NOT NULL DEFAULT 0,
            estoque_minimo  REAL NOT NULL DEFAULT 5,
            preco           REAL DEFAULT 0.0,
            fornecedor_id   INTEGER,
            FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id  INTEGER NOT NULL,
            tipo        TEXT NOT NULL CHECK(tipo IN ('entrada','saida','ajuste')),
            quantidade  REAL NOT NULL,
            data        TEXT NOT NULL,
            usuario_id  INTEGER NOT NULL,
            observacao  TEXT,
            FOREIGN KEY (produto_id)  REFERENCES produtos(id),
            FOREIGN KEY (usuario_id)  REFERENCES usuarios(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id      INTEGER NOT NULL,
            fornecedor_id   INTEGER NOT NULL,
            quantidade      REAL NOT NULL,
            data_pedido     TEXT NOT NULL,
            status          TEXT NOT NULL DEFAULT 'pendente'
                            CHECK(status IN ('pendente','recebido','cancelado')),
            FOREIGN KEY (produto_id)    REFERENCES produtos(id),
            FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
        )
    """)

    cursor.execute("SELECT id FROM usuarios WHERE email = 'admin@stockmaster.com'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, perfil)
            VALUES (?, ?, ?, ?)
        """, ("Administrador", "admin@stockmaster.com", generate_password_hash("admin123"), "admin"))

    conn.commit()
    conn.close()