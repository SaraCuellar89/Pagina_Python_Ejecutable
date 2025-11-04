# database/pedido_dao.py
from database.conexion import get_connection
import uuid

def crear_pedido_con_detalles(usuario_id, carrito):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        codigo = "PED-" + str(uuid.uuid4())[:8]
        cursor.execute(
            "INSERT INTO pedido (codigo, estado, usuario_id) VALUES (?, 'pendiente', ?)",
            (codigo, usuario_id)
        )
        id_pedido = cursor.lastrowid

        for item in carrito:
            cursor.execute(
                "INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad) VALUES (?, ?, ?)",
                (id_pedido, item['id_producto'], item['cantidad'])
            )

            # Opcional: disminuir stock en tabla producto (si lo deseas)
            # cursor.execute("UPDATE producto SET cantidad = cantidad - ? WHERE id_producto = ?", (item['cantidad'], item['id_producto']))

        conn.commit()
        return id_pedido, codigo

    except Exception as e:
        if conn:
            conn.rollback()
        print("Error al crear pedido:", e)
        return None, None
    finally:
        if conn:
            conn.close()


def obtener_pedidos_por_usuario(usuario_id):
    """Devuelve lista de pedidos (id_pedido, codigo, estado, fecha)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_pedido, codigo, estado, fecha FROM pedido WHERE usuario_id = ? ORDER BY fecha DESC", (usuario_id,))
        pedidos = cursor.fetchall()
        conn.close()
        return pedidos
    except Exception as e:
        print("Error al obtener pedidos:", e)
        return []


def obtener_detalle_por_pedido(id_pedido):
    """Devuelve lista de detalles con nombre producto: [(nombre, cantidad, precio), ...]"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pr.nombre, dp.cantidad, pr.precio
            FROM detalle_pedido dp
            JOIN producto pr ON dp.producto_id = pr.id_producto
            WHERE dp.pedido_id = ?
        """, (id_pedido,))
        detalles = cursor.fetchall()
        conn.close()
        return detalles
    except Exception as e:
        print("Error al obtener detalles de pedido:", e)
        return []
