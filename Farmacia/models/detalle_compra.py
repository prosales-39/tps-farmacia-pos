from database.conexion import get_connection

class DetalleCompra:

    @staticmethod
    def crear(compra_id, producto_id, cantidad, precio):
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO detalle_compra (compra_id, producto_id, cantidad, precio)
            VALUES (?, ?, ?, ?)
        """, (compra_id, producto_id, cantidad, precio))
        conexion.commit()
        conexion.close()