import sqlite3
import os
import sys

DB_NAME = "tienda.db"

def get_base_path():
    """Obtiene la ruta base, compatible con PyInstaller"""
    if getattr(sys, 'frozen', False):
        # Si está ejecutándose como .exe (PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # Si se ejecuta como script normal (.py)
        return os.path.dirname(os.path.abspath(__file__))

def get_connection():
    # Carpeta segura para la base de datos (junto al ejecutable)
    base_path = get_base_path()
    db_folder = os.path.join(base_path, "database")

    # Crear carpeta si no existe
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    # Ruta completa al archivo de base de datos
    db_path = os.path.join(db_folder, DB_NAME)
    
    conn = sqlite3.connect(db_path)
    return conn


def crear_tablas():
    """Crea las tablas si no existen aún."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT UNIQUE NOT NULL,
        contrasena TEXT NOT NULL,
        telefono TEXT NOT NULL,
        direccion TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS producto (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        imagen TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedido (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'pendiente',
        usuario_id INTEGER NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuario(id_usuario)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_pedido (
        id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        FOREIGN KEY (pedido_id) REFERENCES pedido(id_pedido) ON DELETE CASCADE,
        FOREIGN KEY (producto_id) REFERENCES producto(id_producto)
    )
    """)

    conn.commit()
    conn.close()
