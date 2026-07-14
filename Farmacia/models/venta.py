from database.conexion import get_connection
from datetime import date

class Venta:

    @staticmethod
    def crear(cliente_id, usuario_id, subtotal, iva, total):
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO ventas (cliente_id, usuario_id, fecha, subtotal, iva, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (cliente_id, usuario_id, date.today().isoformat(), subtotal, iva, total))
        conexion.commit()
        venta_id = cursor.lastrowid
        conexion.close()
        return venta_id