from database.conexion import get_connection
from datetime import datetime, timedelta

class ReportesController:

    @staticmethod
    def obtener_resumen_ventas(fecha_inicio=None, fecha_fin=None):
        """Retorna resumen de ventas en un período."""
        if not fecha_inicio:
            fecha_inicio = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not fecha_fin:
            fecha_fin = datetime.now().strftime("%Y-%m-%d")

        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                COUNT(*) AS total_ventas,
                SUM(total) AS total_ingresos,
                AVG(total) AS promedio_venta,
                SUM(subtotal) AS subtotal,
                SUM(iva) AS total_iva
            FROM ventas
            WHERE fecha BETWEEN ? AND ?
        """, (fecha_inicio, fecha_fin))
        resultado = cursor.fetchone()
        conexion.close()
        return dict(resultado) if resultado else {}

    @staticmethod
    def obtener_productos_mas_vendidos(limite=5):
        """Retorna los productos más vendidos."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                p.nombre,
                SUM(dv.cantidad) AS total_vendido,
                SUM(dv.cantidad * dv.precio) AS total_ingresos
            FROM detalle_venta dv
            INNER JOIN productos p ON dv.producto_id = p.id
            GROUP BY dv.producto_id
            ORDER BY total_vendido DESC
            LIMIT ?
        """, (limite,))
        productos = cursor.fetchall()
        conexion.close()
        return productos

    @staticmethod
    def obtener_ventas_por_dia(dias=7):
        """Retorna ventas agrupadas por día (últimos N días)."""
        fecha_inicio = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                fecha,
                COUNT(*) AS ventas,
                SUM(total) AS ingresos
            FROM ventas
            WHERE fecha >= ?
            GROUP BY fecha
            ORDER BY fecha ASC
        """, (fecha_inicio,))
        datos = cursor.fetchall()
        conexion.close()
        return datos

    @staticmethod
    def obtener_resumen_compras(fecha_inicio=None, fecha_fin=None):
        """Retorna resumen de compras en un período."""
        if not fecha_inicio:
            fecha_inicio = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not fecha_fin:
            fecha_fin = datetime.now().strftime("%Y-%m-%d")

        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                COUNT(*) AS total_compras,
                SUM(total) AS total_gastado,
                AVG(total) AS promedio_compra
            FROM compras
            WHERE fecha BETWEEN ? AND ?
        """, (fecha_inicio, fecha_fin))
        resultado = cursor.fetchone()
        conexion.close()
        return dict(resultado) if resultado else {}

    @staticmethod
    def obtener_productos_stock_bajo():
        """Retorna productos con stock por debajo del mínimo."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                codigo,
                nombre,
                stock,
                stock_minimo
            FROM productos
            WHERE stock <= stock_minimo
            ORDER BY stock ASC
        """)
        productos = cursor.fetchall()
        conexion.close()
        return productos

    @staticmethod
    def obtener_productos_por_vencer(dias=30):
        """Retorna productos que vencen en los próximos N días."""
        fecha_limite = (datetime.now() + timedelta(days=dias)).strftime("%Y-%m-%d")
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                codigo,
                nombre,
                fecha_vencimiento,
                stock
            FROM productos
            WHERE fecha_vencimiento <= ? AND fecha_vencimiento IS NOT NULL
            ORDER BY fecha_vencimiento ASC
        """, (fecha_limite,))
        productos = cursor.fetchall()
        conexion.close()
        return productos

    @staticmethod
    def obtener_ventas_por_usuario():
        """Retorna ventas agrupadas por usuario (vendedor)."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                u.nombre AS usuario,
                COUNT(v.id) AS total_ventas,
                SUM(v.total) AS total_ingresos
            FROM ventas v
            INNER JOIN usuarios u ON v.usuario_id = u.id
            GROUP BY v.usuario_id
            ORDER BY total_ingresos DESC
        """)
        datos = cursor.fetchall()
        conexion.close()
        return datos