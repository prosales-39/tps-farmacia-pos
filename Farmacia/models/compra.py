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

    @staticmethod
    def obtener_por_id(compra_id):
        """Obtiene una compra por su ID."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                c.id,
                c.proveedor_id,
                c.usuario_id,
                c.fecha,
                c.total,
                p.nombre as proveedor_nombre
            FROM compras c
            INNER JOIN proveedores p ON c.proveedor_id = p.id
            WHERE c.id = ?
        """, (compra_id,))
        compra = cursor.fetchone()
        conexion.close()
        return compra