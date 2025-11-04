from database.conexion import get_connection
import os, sys


def get_base_path():
    """Obtiene la ruta base, compatible con PyInstaller"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))
    

def obtener_productos():
    """Obtiene nombre, precio e imagen de cada producto."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, precio, imagen FROM producto")
        productos = cursor.fetchall()  # [(nombre, precio, imagen), ...]
        conn.close()

        base_path = get_base_path()
        productos_ajustados = []
        for nombre, precio, imagen_rel in productos:
            imagen_completa = os.path.join(base_path, imagen_rel)
            productos_ajustados.append((nombre, precio, imagen_completa))
        return productos_ajustados

    except Exception as e:
        print("Error al obtener productos:", e)
        return []

    
def obtener_producto_por_nombre(nombre):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_producto, nombre, cantidad, precio, imagen FROM producto WHERE nombre = ?",
            (nombre,)
        )
        producto = cursor.fetchone()
        conn.close()
        return producto
    except Exception as e:
        print("Error al obtener producto por nombre:", e)
        return None
