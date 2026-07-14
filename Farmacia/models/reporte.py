from database.conexion import get_connection
from datetime import datetime, timedelta

class Reporte:

    @staticmethod
    def ventas_por_periodo(fecha_inicio, fecha_fin):
        """Retorna las ventas agrupadas por día en un periodo."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                fecha,
                COUNT(*) as total_ventas,
                SUM(total) as total_ingresos,
                SUM(subtotal) as subtotal,
                SUM(iva) as total_iva
            FROM ventas
            WHERE fecha BETWEEN ? AND ?
            GROUP BY fecha
            ORDER BY fecha DESC
        """, (fecha_inicio, fecha_fin))
        resultados = cursor.fetchall()
        conexion.close()
        return resultados

    @staticmethod
    def ventas_por_mes(mes, año):
        """Retorna el resumen de ventas de un mes específico."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total_ventas,
                SUM(total) as total_ingresos,
                SUM(subtotal) as subtotal,
                SUM(iva) as total_iva
            FROM ventas
            WHERE strftime('%m', fecha) = ? AND strftime('%Y', fecha) = ?
        """, (f"{mes:02d}", str(año)))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado

    @staticmethod
    def productos_mas_vendidos(fecha_inicio, fecha_fin, limite=10):
        """Retorna los productos más vendidos en un periodo."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                p.nombre,
                SUM(dv.cantidad) as total_vendido,
                SUM(dv.cantidad * dv.precio) as total_ingresos
            FROM detalle_venta dv
            INNER JOIN productos p ON dv.producto_id = p.id
            INNER JOIN ventas v ON dv.venta_id = v.id
            WHERE v.fecha BETWEEN ? AND ?
            GROUP BY dv.producto_id
            ORDER BY total_vendido DESC
            LIMIT ?
        """, (fecha_inicio, fecha_fin, limite))
        resultados = cursor.fetchall()
        conexion.close()
        return resultados

    @staticmethod
    def compras_por_periodo(fecha_inicio, fecha_fin):
        """Retorna las compras agrupadas por día en un periodo."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                fecha,
                COUNT(*) as total_compras,
                SUM(total) as total_gastos
            FROM compras
            WHERE fecha BETWEEN ? AND ?
            GROUP BY fecha
            ORDER BY fecha DESC
        """, (fecha_inicio, fecha_fin))
        resultados = cursor.fetchall()
        conexion.close()
        return resultados

    @staticmethod
    def resumen_inventario():
        """Retorna estadísticas del inventario."""
        conexion = get_connection()
        cursor = conexion.cursor()
        
        # Total productos
        cursor.execute("SELECT COUNT(*) as total FROM productos")
        total_productos = cursor.fetchone()["total"]
        
        # Stock bajo (stock < stock_minimo)
        cursor.execute("""
            SELECT COUNT(*) as bajo_stock 
            FROM productos 
            WHERE stock < stock_minimo
        """)
        bajo_stock = cursor.fetchone()["bajo_stock"]
        
        # Productos por vencer (próximos 30 días)
        from datetime import date, timedelta
        hoy = date.today().isoformat()
        dentro_30 = (date.today() + timedelta(days=30)).isoformat()
        cursor.execute("""
            SELECT COUNT(*) as por_vencer
            FROM productos
            WHERE fecha_vencimiento BETWEEN ? AND ?
        """, (hoy, dentro_30))
        por_vencer = cursor.fetchone()["por_vencer"]
        
        # Valor total del inventario
        cursor.execute("SELECT SUM(precio * stock) as valor_total FROM productos")
        valor_total = cursor.fetchone()["valor_total"] or 0
        
        conexion.close()
        return {
            "total_productos": total_productos,
            "bajo_stock": bajo_stock,
            "por_vencer": por_vencer,
            "valor_total": valor_total
        }

    @staticmethod
    def ventas_por_usuario(fecha_inicio, fecha_fin):
        """Retorna las ventas realizadas por cada usuario en un periodo."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                u.nombre as usuario,
                COUNT(v.id) as total_ventas,
                SUM(v.total) as total_ingresos
            FROM ventas v
            INNER JOIN usuarios u ON v.usuario_id = u.id
            WHERE v.fecha BETWEEN ? AND ?
            GROUP BY v.usuario_id
            ORDER BY total_ingresos DESC
        """, (fecha_inicio, fecha_fin))
        resultados = cursor.fetchall()
        conexion.close()
        return resultados