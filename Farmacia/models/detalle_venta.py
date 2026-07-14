from database.conexion import get_connection

class DetalleVenta:

    @staticmethod
    def crear(venta_id, producto_id, cantidad, precio):
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio)
            VALUES (?, ?, ?, ?)
        """, (venta_id, producto_id, cantidad, precio))
        conexion.commit()
        conexion.close()