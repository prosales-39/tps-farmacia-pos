from database.conexion import get_connection
from datetime import date

class Factura:
    
    @staticmethod
    def generar_numero_factura():
        """Genera el siguiente número de factura: F-ANO-MES-CONSECUTIVO"""
        anio = date.today().strftime("%Y")
        mes = date.today().strftime("%m")
        
        conexion = get_connection()
        cursor = conexion.cursor()
        
        # Buscar el último número del mes actual
        cursor.execute("""
            SELECT numero_factura 
            FROM facturas 
            WHERE numero_factura LIKE ?
            ORDER BY id DESC 
            LIMIT 1
        """, (f"F-{anio}-{mes}-%",))
        
        ultimo = cursor.fetchone()
        conexion.close()
        
        if ultimo:
            # Extraer el consecutivo: F-2026-07-0001 -> 0001
            partes = ultimo["numero_factura"].split("-")
            consecutivo = int(partes[3]) + 1
        else:
            consecutivo = 1
        
        return f"F-{anio}-{mes}-{consecutivo:04d}"
    
    @staticmethod
    def crear(venta_id, subtotal, iva, total, cliente_nombre=None, cliente_documento=None):
        """Crea una nueva factura a partir de una venta."""
        conexion = get_connection()
        cursor = conexion.cursor()
        
        numero_factura = Factura.generar_numero_factura()
        fecha_emision = date.today().isoformat()
        
        cursor.execute("""
            INSERT INTO facturas (
                venta_id, numero_factura, fecha_emision,
                subtotal, iva, total, cliente_nombre, cliente_documento, estado
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            venta_id, numero_factura, fecha_emision,
            subtotal, iva, total, cliente_nombre, cliente_documento, 'ACTIVA'
        ))
        
        conexion.commit()
        factura_id = cursor.lastrowid
        conexion.close()
        
        return factura_id, numero_factura
    
    @staticmethod
    def obtener_por_venta(venta_id):
        """Obtiene la factura asociada a una venta."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT * FROM facturas WHERE venta_id = ?
        """, (venta_id,))
        factura = cursor.fetchone()
        conexion.close()
        return factura
    
    @staticmethod
    def obtener_ultimas(limite=10):
        """Obtiene las últimas facturas generadas."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                f.*,
                v.id as venta_id
            FROM facturas f
            INNER JOIN ventas v ON f.venta_id = v.id
            ORDER BY f.id DESC
            LIMIT ?
        """, (limite,))
        facturas = cursor.fetchall()
        conexion.close()
        return facturas
    
    @staticmethod
    def anular(factura_id):
        """Anula una factura (cambia estado a ANULADA)."""
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE facturas SET estado = 'ANULADA'
            WHERE id = ?
        """, (factura_id,))
        conexion.commit()
        conexion.close()