from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from pathlib import Path
import os

class ComprobanteCompra:
    """Genera comprobantes de compra en PDF con formato profesional."""

    COMPROBANTES_DIR = "comprobantes"

    @classmethod
    def _asegurar_directorio(cls):
        comp_dir = Path(cls.COMPROBANTES_DIR)
        comp_dir.mkdir(exist_ok=True)
        return comp_dir

    @classmethod
    def generar(cls, compra, items, proveedor, usuario):
        """
        Genera un comprobante de compra en PDF con formato profesional.
        """
        comp_dir = cls._asegurar_directorio()
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"compra_{compra['id']}_{fecha}.pdf"
        ruta = comp_dir / nombre_archivo

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

        # ============ TÍTULO COMPROBANTE ============
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.HexColor("#1565C0"))
        c.drawString(50, height - 160, "COMPROBANTE DE COMPRA")

        # ============ DATOS DE LA COMPRA ============
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        c.drawString(50, height - 180, f"Compra #: {compra['id']}")
        c.drawString(50, height - 195, f"Fecha: {compra['fecha']}")
        c.drawString(350, height - 180, f"Total: ${compra['total']:,.0f}".replace(",", "."))

        # ============ DATOS DEL PROVEEDOR ============
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, height - 225, "DATOS DEL PROVEEDOR")
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 245, f"Nombre: {proveedor['nombre']}")
        c.drawString(50, height - 260, f"Teléfono: {proveedor['telefono'] or 'N/A'}")
        c.drawString(50, height - 275, f"Correo: {proveedor['correo'] or 'N/A'}")
        c.drawString(50, height - 290, f"Dirección: {proveedor['direccion'] or 'N/A'}")

        # ============ DATOS DEL USUARIO ============
        c.setFont("Helvetica-Bold", 11)
        c.drawString(350, height - 225, "REGISTRADO POR")
        c.setFont("Helvetica", 10)
        c.drawString(350, height - 245, f"Usuario: {usuario['nombre']}")
        c.drawString(350, height - 260, f"ID: {usuario['id']}")

        # ============ TABLA DE PRODUCTOS ============
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, height - 320, "PRODUCTOS COMPRADOS")

        # Datos de la tabla
        data = [["Cant.", "Producto", "Lote", "Precio", "Subtotal"]]
        total = 0
        for item in items:
            sub = item["cantidad"] * item["precio_unitario"]
            total += sub
            data.append([
                str(item["cantidad"]),
                item.get("nombre", "Producto"),
                item.get("lote", "N/A"),
                f"${item['precio_unitario']:,.0f}".replace(",", "."),
                f"${sub:,.0f}".replace(",", ".")
            ])

        # Tabla
        tabla = Table(data, colWidths=[50, 180, 80, 80, 80])
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
        tabla.drawOn(c, 50, height - 450)

        # ============ TOTAL ============
        y_total = height - 470
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.HexColor("#1565C0"))
        c.drawString(350, y_total, f"TOTAL COMPRA: ${total:,.0f}".replace(",", "."))

        # ============ PIE DE PÁGINA ============
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.grey)
        c.drawString(50, 50, "Este comprobante es un registro de la transacción realizada en el sistema Farmacia POS.")
        c.drawString(50, 35, f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        c.drawString(50, 20, "© 2026 Farmacia POS - Todos los derechos reservados")

        c.save()
        return str(ruta)