import tkinter as tk
from tkinter import ttk, messagebox
from models.factura import Factura
from database.conexion import get_connection
from utils.helpers import formatear_precio

class FacturasView:

    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.crear_interfaz()
        self.cargar_facturas()

    def crear_interfaz(self):
        tk.Label(
            self.contenedor,
            text="📄 Facturas Electrónicas",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#1565C0"
        ).pack(pady=(10, 5))

        # Frame para filtros
        frame_filtros = tk.Frame(self.contenedor, bg="white")
        frame_filtros.pack(fill="x", padx=20, pady=10)

        tk.Button(
            frame_filtros,
            text="🔄 Actualizar",
            command=self.cargar_facturas,
            bg="#1565C0",
            fg="white",
            relief="flat",
            padx=15
        ).pack(side="left", padx=5)

        tk.Button(
            frame_filtros,
            text="📥 Exportar PDF",
            command=self.exportar_pdf,
            bg="#43A047",
            fg="white",
            relief="flat",
            padx=15
        ).pack(side="left", padx=5)

        # Tabla de facturas
        frame_tabla = tk.Frame(self.contenedor, bg="white")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("N° Factura", "Fecha", "Cliente", "Subtotal", "IVA", "Total", "Estado")
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=18
        )

        self.tabla.heading("N° Factura", text="N° Factura")
        self.tabla.heading("Fecha", text="Fecha")
        self.tabla.heading("Cliente", text="Cliente")
        self.tabla.heading("Subtotal", text="Subtotal")
        self.tabla.heading("IVA", text="IVA")
        self.tabla.heading("Total", text="Total")
        self.tabla.heading("Estado", text="Estado")

        self.tabla.column("N° Factura", width=120, anchor="center")
        self.tabla.column("Fecha", width=100, anchor="center")
        self.tabla.column("Cliente", width=150, anchor="w")
        self.tabla.column("Subtotal", width=100, anchor="e")
        self.tabla.column("IVA", width=100, anchor="e")
        self.tabla.column("Total", width=100, anchor="e")
        self.tabla.column("Estado", width=80, anchor="center")

        self.tabla.pack(fill="both", expand=True)

        # Botones de acción
        frame_botones = tk.Frame(self.contenedor, bg="white")
        frame_botones.pack(fill="x", padx=20, pady=10)

        tk.Button(
            frame_botones,
            text="📄 Ver Detalle",
            command=self.ver_detalle,
            bg="#1565C0",
            fg="white",
            relief="flat",
            padx=15
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botones,
            text="❌ Anular Factura",
            command=self.anular_factura,
            bg="#E53935",
            fg="white",
            relief="flat",
            padx=15
        ).pack(side="left", padx=5)

    def cargar_facturas(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        facturas = Factura.obtener_ultimas(50)
        for f in facturas:
            estado = f["estado"]
            self.tabla.insert(
                "",
                "end",
                values=(
                    f["numero_factura"],
                    f["fecha_emision"],
                    f["cliente_nombre"] or "Mostrador",
                    formatear_precio(f["subtotal"]),
                    formatear_precio(f["iva"]),
                    formatear_precio(f["total"]),
                    estado
                ),
                tags=(f["id"], estado)
            )

        # Configurar colores de estado
        self.tabla.tag_configure("ACTIVA", foreground="green")
        self.tabla.tag_configure("ANULADA", foreground="red")

    def ver_detalle(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Seleccionar", "Seleccione una factura")
            return

        item = self.tabla.item(seleccion[0])
        factura_id = item["tags"][0]

        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM facturas WHERE id = ?", (factura_id,))
        factura = cursor.fetchone()
        conexion.close()

        if not factura:
            messagebox.showerror("Error", "Factura no encontrada")
            return

        detalle = f"""
        📄 FACTURA ELECTRÓNICA
        =======================
        Número: {factura['numero_factura']}
        Fecha: {factura['fecha_emision']}
        Cliente: {factura['cliente_nombre'] or 'Mostrador'}
        Documento: {factura['cliente_documento'] or 'N/A'}
        Estado: {factura['estado']}

        -----------------------
        Subtotal: {formatear_precio(factura['subtotal'])}
        IVA (19%): {formatear_precio(factura['iva'])}
        TOTAL: {formatear_precio(factura['total'])}
        =======================
        """
        messagebox.showinfo(f"Factura {factura['numero_factura']}", detalle)

    def anular_factura(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Seleccionar", "Seleccione una factura")
            return

        item = self.tabla.item(seleccion[0])
        factura_id = item["tags"][0]
        estado = item["values"][6]

        if estado == "ANULADA":
            messagebox.showwarning("Ya anulada", "Esta factura ya está anulada")
            return

        if messagebox.askyesno("Confirmar", "¿Anular esta factura?"):
            try:
                Factura.anular(factura_id)
                self.cargar_facturas()
                messagebox.showinfo("Éxito", "Factura anulada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo anular: {e}")

    def exportar_pdf(self):
        """Exporta la factura seleccionada a PDF."""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from datetime import datetime
            from tkinter import filedialog

            seleccion = self.tabla.selection()
            if not seleccion:
                messagebox.showwarning("Seleccionar", "Seleccione una factura")
                return

            item = self.tabla.item(seleccion[0])
            factura_id = item["tags"][0]

            conexion = get_connection()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM facturas WHERE id = ?", (factura_id,))
            factura = cursor.fetchone()
            conexion.close()

            if not factura:
                messagebox.showerror("Error", "Factura no encontrada")
                return

            archivo = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"factura_{factura['numero_factura']}.pdf"
            )

            if not archivo:
                return

            c = canvas.Canvas(archivo, pagesize=A4)
            width, height = A4

            # Título
            c.setFont("Helvetica-Bold", 20)
            c.drawString(200, height - 50, "FACTURA ELECTRÓNICA")

            # Datos
            c.setFont("Helvetica", 12)
            y = height - 100
            c.drawString(50, y, f"Número: {factura['numero_factura']}")
            y -= 25
            c.drawString(50, y, f"Fecha: {factura['fecha_emision']}")
            y -= 25
            c.drawString(50, y, f"Cliente: {factura['cliente_nombre'] or 'Mostrador'}")
            y -= 25
            c.drawString(50, y, f"Documento: {factura['cliente_documento'] or 'N/A'}")
            y -= 25
            c.drawString(50, y, f"Estado: {factura['estado']}")

            # Línea separadora
            y -= 25
            c.line(50, y, 550, y)
            y -= 25

            # Totales
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, f"Subtotal: {formatear_precio(factura['subtotal'])}")
            y -= 25
            c.drawString(50, y, f"IVA (19%): {formatear_precio(factura['iva'])}")
            y -= 25
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, f"TOTAL: {formatear_precio(factura['total'])}")

            # Pie de página
            c.setFont("Helvetica", 10)
            c.drawString(50, 50, "Gracias por su compra")
            c.drawString(50, 35, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            c.save()
            messagebox.showinfo("Éxito", f"PDF generado:\n{archivo}")

        except ImportError:
            messagebox.showerror(
                "Error de dependencia",
                "La librería 'reportlab' no está instalada.\nEjecute: pip install reportlab"
            )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")