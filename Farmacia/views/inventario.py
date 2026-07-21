import tkinter as tk
from tkinter import ttk, messagebox
from controllers.inventario_controller import InventarioController
from utils.helpers import formatear_precio
from views.formulario_producto import FormularioProducto

class InventarioView:

    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.id_seleccionado = None
        self.crear_busqueda()
        self.crear_tabla()
        self.crear_botones()
        self.cargar_tabla()

    def crear_busqueda(self):
        frame = tk.Frame(self.contenedor, bg="white")
        frame.pack(fill="x", padx=20, pady=10)

        tk.Label(frame, text="🔍 Buscar:", bg="white", font=("Segoe UI", 11)).pack(side="left", padx=(0, 10))
        self.entry_busqueda = tk.Entry(frame, font=("Segoe UI", 11), width=40)
        self.entry_busqueda.pack(side="left", padx=(0, 10))
        self.entry_busqueda.bind("<KeyRelease>", self.buscar_automatico)

        tk.Button(
            frame,
            text="Buscar",
            command=self.buscar_automatico,
            bg="#1565C0",
            fg="white",
            font=("Segoe UI", 10),
            relief="flat",
            padx=10
        ).pack(side="left")

        tk.Button(
            frame,
            text="Limpiar",
            command=self.limpiar_busqueda,
            bg="#78909C",
            fg="white",
            font=("Segoe UI", 10),
            relief="flat",
            padx=10
        ).pack(side="left", padx=(10, 0))

    def crear_tabla(self):
        frame_tabla = tk.Frame(self.contenedor, bg="white")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal")

        columnas = ("Código", "Nombre", "Stock", "Precio", "Vencimiento", "Lote")
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=18
        )

        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        self.tabla.heading("Código", text="Código")
        self.tabla.heading("Nombre", text="Medicamento")
        self.tabla.heading("Stock", text="Stock")
        self.tabla.heading("Precio", text="Precio")
        self.tabla.heading("Vencimiento", text="Vencimiento")
        self.tabla.heading("Lote", text="Lote")

        self.tabla.column("Código", width=100, anchor="center")
        self.tabla.column("Nombre", width=200, anchor="w")
        self.tabla.column("Stock", width=80, anchor="center")
        self.tabla.column("Precio", width=100, anchor="e")
        self.tabla.column("Vencimiento", width=120, anchor="center")
        self.tabla.column("Lote", width=100, anchor="center")

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        self.tabla.bind("<<TreeviewSelect>>", self.on_seleccionar)

    def crear_botones(self):
        frame = tk.Frame(self.contenedor, bg="white")
        frame.pack(fill="x", padx=20, pady=(0, 20))

        botones = [
            ("➕ Nuevo", self.nuevo_producto),
            ("✏️ Editar", self.editar_producto),
            ("🗑️ Eliminar", self.eliminar_producto),
            ("🔄 Actualizar", self.cargar_tabla),
            ("📥 Exportar Excel", self.exportar_excel)
        ]

        for texto, comando in botones:
            tk.Button(
                frame,
                text=texto,
                command=comando,
                relief="flat",
                bg="#E3F2FD",
                fg="#0D47A1",
                font=("Segoe UI", 10, "bold"),
                padx=15,
                pady=5
            ).pack(side="left", padx=(0, 10))

    def cargar_tabla(self, productos=None):
        # Limpiar tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        if productos is None:
            productos = InventarioController.listar_productos()

        for p in productos:
            self.tabla.insert(
                "",
                "end",
                values=(
                    p["codigo"],
                    p["nombre"],
                    p["stock"],
                    formatear_precio(p["precio"]),
                    p["fecha_vencimiento"] or "",
                    p["lote"] or ""
                ),
                tags=(p["id"],)
            )

    def buscar_automatico(self, event=None):
        termino = self.entry_busqueda.get().strip()
        if termino:
            productos = InventarioController.buscar_productos(termino)
        else:
            productos = InventarioController.listar_productos()
        self.cargar_tabla(productos)

    def limpiar_busqueda(self):
        self.entry_busqueda.delete(0, tk.END)
        self.cargar_tabla()

    def on_seleccionar(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            self.id_seleccionado = item["tags"][0] if item["tags"] else None
        else:
            self.id_seleccionado = None

    def nuevo_producto(self):
        """Abre el formulario para crear un nuevo producto."""
        FormularioProducto(
            parent=self.contenedor.winfo_toplevel(),
            producto_id=None,
            callback_guardar=self.cargar_tabla
        )

    def editar_producto(self):
        """Abre el formulario para editar el producto seleccionado."""
        if not self.id_seleccionado:
            messagebox.showwarning("Seleccionar", "Primero selecciona un producto")
            return

        FormularioProducto(
            parent=self.contenedor.winfo_toplevel(),
            producto_id=self.id_seleccionado,
            callback_guardar=self.cargar_tabla
        )

    def eliminar_producto(self):
        """Elimina el producto seleccionado."""
        if not self.id_seleccionado:
            messagebox.showwarning("Seleccionar", "Primero selecciona un producto")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar este producto?"):
            try:
                InventarioController.eliminar_producto(self.id_seleccionado)
                self.cargar_tabla()
                self.id_seleccionado = None
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def exportar_excel(self):
        """Exporta los datos de la tabla visible a un archivo XLSX."""
        try:
            import openpyxl
            from tkinter import filedialog
            from datetime import datetime

            archivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")],
                initialfile=f"inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )

            if not archivo:
                return

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Inventario"

            # Escribir encabezados
            columnas = [self.tabla.heading(col)["text"] for col in self.tabla["columns"]]
            ws.append(columnas)

            # Escribir datos
            for item in self.tabla.get_children():
                valores = self.tabla.item(item)["values"]
                ws.append(valores)

            wb.save(archivo)
            messagebox.showinfo("Exportación exitosa", f"Archivo guardado en:\n{archivo}")

        except ImportError:
            messagebox.showerror("Error de dependencia", "La librería 'openpyxl' no está instalada.\nEjecute: pip install openpyxl")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")