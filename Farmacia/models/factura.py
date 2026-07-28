from database.conexion import get_connection
from datetime import date
import os
from pathlib import Path

class Factura:

    @staticmethod
    def generar_numero_factura():
        """Genera el siguiente número de factura: F-ANO-MES-CONSECUTIVO"""
        anio = date.today().strftime("%Y")
        mes = date.today().strftime("%m")
        
        conexion = get_connection()
        cursor = conexion.cursor()
        
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
            partes = ultimo["numero_factura"].split("-")
            consecutivo = int(partes[3]) + 1
        else:
            consecutivo = 1
        
        return f"F-{anio}-{mes}-{consecutivo:04d}"
    
    @staticmethod
    def crear(venta_id, subtotal, iva, total, cliente_nombre=None, cliente_documento=None):
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
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM facturas WHERE venta_id = ?", (venta_id,))
        factura = cursor.fetchone()
        conexion.close()
        return factura
    
    @staticmethod
    def obtener_ultimas(limite=10):
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
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE facturas SET estado = 'ANULADA'
            WHERE id = ?
        """, (factura_id,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def generar_pdf_factura(factura_id):
        """Genera un PDF con el formato profesional de la factura."""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from reportlab.lib import colors
            from reportlab.platypus import Table, TableStyle
            from datetime import datetime
            import sqlite3
            from database.conexion import get_connection
            
            # Obtener datos de la factura
            conexion = get_connection()
            cursor = conexion.cursor()
            
            cursor.execute("""
                SELECT 
                    f.*,
                    v.fecha as venta_fecha
                FROM facturas f
                INNER JOIN ventas v ON f.venta_id = v.id
                WHERE f.id = ?
            """, (factura_id,))
            factura = cursor.fetchone()
            
            if not factura:
                conexion.close()
                return None
            
            # Obtener detalles de la venta
            cursor.execute("""
                SELECT 
                    p.nombre as producto,
                    dv.cantidad,
                    dv.precio,
                    (dv.cantidad * dv.precio) as subtotal
                FROM detalle_venta dv
                INNER JOIN productos p ON dv.producto_id = p.id
                WHERE dv.venta_id = ?
            """, (factura['venta_id'],))
            detalles = cursor.fetchall()
            conexion.close()
            
            # Crear directorio si no existe
            facturas_dir = Path("facturas_pdf")
            facturas_dir.mkdir(exist_ok=True)
            
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"factura_{factura['numero_factura']}_{fecha_actual}.pdf"
            ruta = facturas_dir / nombre_archivo
            
            # Crear PDF
            c = canvas.Canvas(str(ruta), pagesize=A4)
            width, height = A4
            
            # ============ ENCABEZADO ============
            # Título
            c.setFont("Helvetica-Bold", 24)
            c.setFillColor(colors.HexColor("#1565C0"))
            c.drawString(50, height - 50, "FARMACIA POS")
            
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.black)
            c.drawString(50, height - 70, "Sistema de Gestión Farmacéutica")
            c.drawString(50, height - 85, "NIT: 900.123.456-7")
            c.drawString(50, height - 100, "Dirección: Calle 123 #45-67, Bogotá")
            c.drawString(50, height - 115, "Teléfono: (601) 123-4567")
            
            # Línea separadora
            c.setStrokeColor(colors.HexColor("#1565C0"))
            c.setLineWidth(2)
            c.line(50, height - 130, 550, height - 130)
            
            # ============ DATOS DE LA FACTURA ============
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.HexColor("#1565C0"))
            c.drawString(50, height - 160, "FACTURA ELECTRÓNICA")
            
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.black)
            c.drawString(50, height - 180, f"Número: {factura['numero_factura']}")
            c.drawString(50, height - 195, f"Fecha: {factura['fecha_emision']}")
            c.drawString(350, height - 180, f"Venta #: {factura['venta_id']}")
            c.drawString(350, height - 195, f"Estado: {factura['estado']}")
            
            # ============ DATOS DEL CLIENTE ============
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, height - 225, "DATOS DEL CLIENTE")
            c.setFont("Helvetica", 10)
            c.drawString(50, height - 245, f"Nombre: {factura['cliente_nombre'] or 'Cliente Mostrador'}")
            c.drawString(50, height - 260, f"Documento: {factura['cliente_documento'] or 'N/A'}")
            
            # ============ TABLA DE PRODUCTOS ============
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, height - 290, "DETALLE DE PRODUCTOS")
            
            # Datos de la tabla
            data = [["Cant.", "Producto", "Precio Unit.", "Subtotal"]]
            for detalle in detalles:
                data.append([
                    str(detalle['cantidad']),
                    detalle['producto'],
                    f"${detalle['precio']:,.0f}".replace(",", "."),
                    f"${detalle['subtotal']:,.0f}".replace(",", ".")
                ])
            
            # Tabla
            tabla = Table(data, colWidths=[50, 250, 90, 90])
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1565C0")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            
            # Posicionar tabla
            tabla.wrapOn(c, width, height)
            tabla.drawOn(c, 50, height - 430)
            
            # ============ TOTALES ============
            y_total = height - 450
            c.setFont("Helvetica-Bold", 12)
            c.drawString(350, y_total, f"Subtotal: ${factura['subtotal']:,.0f}".replace(",", "."))
            y_total -= 20
            c.drawString(350, y_total, f"IVA (19%): ${factura['iva']:,.0f}".replace(",", "."))
            y_total -= 25
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.HexColor("#1565C0"))
            c.drawString(350, y_total, f"TOTAL: ${factura['total']:,.0f}".replace(",", "."))
            
            # ============ PIE DE PÁGINA ============
            c.setFont("Helvetica", 8)
            c.setFillColor(colors.grey)
            c.drawString(50, 50, "Este documento es una factura electrónica válida para todos los efectos legales.")
            c.drawString(50, 35, f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            c.drawString(50, 20, "© 2026 Farmacia POS - Todos los derechos reservados")
            
            c.save()
            return str(ruta)
            
        except Exception as e:
            print(f"Error al generar PDF de factura: {e}")
            return None