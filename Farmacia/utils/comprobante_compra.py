from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from pathlib import Path
import os

class ComprobanteCompra:
    """Genera comprobantes de compra en PDF."""

    COMPROBANTES_DIR = "comprobantes"

    @classmethod
    def _asegurar_directorio(cls):
        """Asegura que el directorio de comprobantes existe."""
        comp_dir = Path(cls.COMPROBANTES_DIR)
        comp_dir.mkdir(exist_ok=True)
        return comp_dir

    @classmethod
    def generar(cls, compra, items, proveedor, usuario):
        """
        Genera un comprobante de compra en PDF.
        """
        comp_dir = cls._asegurar_directorio()
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"compra_{compra['id']}_{fecha}.pdf"
        ruta = comp_dir / nombre_archivo

        c = canvas.Canvas(str(ruta), pagesize=A4)
        width, height = A4

        # ============ ENCABEZADO ============
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "COMPROBANTE DE COMPRA")

        c.setFont("Helvetica", 10)
        c.drawString(50, height - 70, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        c.drawString(50, height - 85, f"Compra #: {compra['id']}")

        # Línea separadora
        c.line(50, height - 95, 550, height - 95)

        # ============ DATOS DEL PROVEEDOR ============
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 120, "PROVEEDOR")
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 140, f"Nombre: {proveedor['nombre']}")
        c.drawString(50, height - 155, f"Teléfono: {proveedor['telefono'] or 'N/A'}")
        c.drawString(50, height - 170, f"Correo: {proveedor['correo'] or 'N/A'}")

        # ============ DATOS DEL USUARIO ============
        c.setFont("Helvetica-Bold", 12)
        c.drawString(350, height - 120, "REGISTRADO POR")
        c.setFont("Helvetica", 10)
        c.drawString(350, height - 140, f"Usuario: {usuario['nombre']}")
        c.drawString(350, height - 155, f"ID: {usuario['id']}")

        # ============ TABLA DE PRODUCTOS ============
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 200, "PRODUCTOS")

        # Datos de la tabla
        data = [["Cant.", "Producto", "Lote", "Precio", "Subtotal"]]
        total = 0
        for item in items:
            sub = item["cantidad"] * item["precio_unitario"]
            total += sub
            data.append([
                str(item["cantidad"]),
                item["nombre"],
                item.get("lote", "N/A"),
                f"${item['precio_unitario']:,.0f}".replace(",", "."),
                f"${sub:,.0f}".replace(",", ".")
            ])

        # Tabla
        tabla = Table(data, colWidths=[50, 180, 80, 80, 80])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Posicionar tabla
        tabla.wrapOn(c, width, height)
        tabla.drawOn(c, 50, height - 420)

        # ============ TOTAL ============
        y_total = height - 440
        c.setFont("Helvetica-Bold", 12)
        c.drawString(350, y_total, f"TOTAL COMPRA: ${total:,.0f}".replace(",", "."))

        # ============ PIE DE PÁGINA ============
        c.setFont("Helvetica", 8)
        c.drawString(50, 50, "Este comprobante es un registro de la transacción realizada en el sistema Farmacia POS.")
        c.drawString(50, 35, f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        c.save()
        return str(ruta)