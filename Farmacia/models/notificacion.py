from database.conexion import get_connection

class Notificacion:

    @staticmethod
    def verificar_stock_bajo():
        """
        Verifica los productos con stock por debajo del mínimo.
        Retorna una lista de productos críticos.
        """
        conexion = get_connection()
        cursor = conexion.cursor()
        
        cursor.execute("""
            SELECT 
                id,
                codigo,
                nombre,
                stock,
                stock_minimo,
                (stock_minimo - stock) AS faltante
            FROM productos
            WHERE stock <= stock_minimo
            ORDER BY (stock_minimo - stock) DESC
        """)
        
        productos = cursor.fetchall()
        conexion.close()
        return productos

    @staticmethod
    def contar_stock_bajo():
        """Retorna el número de productos con stock bajo."""
        productos = Notificacion.verificar_stock_bajo()
        return len(productos)