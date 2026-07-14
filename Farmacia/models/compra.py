from database.conexion import get_connection
from datetime import date

class Compra:

    @staticmethod
    def crear(proveedor_id, usuario_id, total):
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO compras (proveedor_id, usuario_id, fecha, total)
            VALUES (?, ?, ?, ?)
        """, (proveedor_id, usuario_id, date.today().isoformat(), total))
        conexion.commit()
        compra_id = cursor.lastrowid
        conexion.close()
        return compra_id