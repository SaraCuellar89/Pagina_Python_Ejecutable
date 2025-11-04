from database.conexion import get_connection

def registrar_usuario(nombre, correo, contrasena, telefono, direccion):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuario (nombre, correo, contrasena, telefono, direccion)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, correo, contrasena, telefono, direccion))
        conn.commit()
        return True
    except Exception as e:
        print("Error al registrar usuario:", e)
        return False
    finally:
        conn.close()


import sqlite3

def verificar_usuario(correo, contrasena):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuario WHERE correo = ? AND contrasena = ?", (correo, contrasena))
        usuario = cursor.fetchone()
        conexion.close()
        return usuario  # Devuelve la fila del usuario si existe
    except Exception as e:
        print("Error al verificar usuario:", e)
        return None

