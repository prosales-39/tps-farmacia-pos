import tkinter as tk
from tkinter import ttk, messagebox
from controllers.inventario_controller import InventarioController

class FormularioProducto:

    def __init__(self, parent, producto_id=None, callback_guardar=None):
        """
        parent: ventana padre (Toplevel o Tk)
        producto_id: si se pasa, es modo edición; si no, modo nuevo.
        callback_guardar: función que se ejecutará después de guardar (para refrescar tabla)
        """
        self.parent = parent
        self.producto_id = producto_id
        self.callback = callback_guardar
        self.datos_iniciales = None

        # Ventana emergente
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Nuevo Producto" if producto_id is None else "Editar Producto")
        self.ventana.geometry("500x600")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()  # Modal

        self.crear_widgets()

        # Si es edición, cargar datos
        if producto_id:
            self.cargar_datos()

    def crear_widgets(self):
        frame = tk.Frame(self.ventana, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Campos
        campos = [
            ("Código:", "codigo"),
            ("Nombre:", "nombre"),
            ("Categoría:", "categoria"),
            ("Precio:", "precio"),
            ("Stock:", "stock"),
            ("Stock mínimo:", "stock_minimo"),
            ("Fecha vencimiento (YYYY-MM-DD):", "fecha_vencimiento"),
            ("Lote:", "lote"),
        ]

        self.entries = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(frame, text=label, font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(frame, font=("Segoe UI", 10), width=30)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries[key] = entry

        # Checkbox para receta
        self.receta_var = tk.IntVar()
        tk.Checkbutton(
            frame,
            text="Requiere receta médica",
            variable=self.receta_var,
            font=("Segoe UI", 10)
        ).grid(row=len(campos), column=0, columnspan=2, pady=10, sticky="w")

        # Botones
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

        tk.Button(
            btn_frame,
            text="Guardar",
            command=self.guardar,
            bg="#1565C0",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=5
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Cancelar",
            command=self.ventana.destroy,
            bg="#78909C",
            fg="white",
            font=("Segoe UI", 10),
            relief="flat",
            padx=20,
            pady=5
        ).pack(side="left", padx=10)

    def cargar_datos(self):
        """Carga los datos del producto existente en los campos."""
        from models.producto import Producto
        producto = Producto.obtener_por_id(self.producto_id)
        if producto:
            self.entries["codigo"].insert(0, producto["codigo"])
            self.entries["nombre"].insert(0, producto["nombre"])
            self.entries["categoria"].insert(0, producto["categoria"] or "")
            self.entries["precio"].insert(0, str(producto["precio"]))
            self.entries["stock"].insert(0, str(producto["stock"]))
            self.entries["stock_minimo"].insert(0, str(producto["stock_minimo"]))
            self.entries["fecha_vencimiento"].insert(0, producto["fecha_vencimiento"] or "")
            self.entries["lote"].insert(0, producto["lote"] or "")
            self.receta_var.set(producto["requiere_receta"])
        else:
            messagebox.showerror("Error", "No se encontró el producto.")
            self.ventana.destroy()

    def guardar(self):
        # Obtener datos
        datos = {
            "codigo": self.entries["codigo"].get().strip(),
            "nombre": self.entries["nombre"].get().strip(),
            "categoria": self.entries["categoria"].get().strip(),
            "precio": self.entries["precio"].get().strip(),
            "stock": self.entries["stock"].get().strip(),
            "stock_minimo": self.entries["stock_minimo"].get().strip(),
            "fecha_vencimiento": self.entries["fecha_vencimiento"].get().strip(),
            "lote": self.entries["lote"].get().strip(),
            "requiere_receta": self.receta_var.get()
        }

        # Validaciones básicas
        if not datos["codigo"] or not datos["nombre"]:
            messagebox.showwarning("Campos incompletos", "Código y Nombre son obligatorios.")
            return

        try:
            datos["precio"] = float(datos["precio"])
            datos["stock"] = int(datos["stock"])
            datos["stock_minimo"] = int(datos["stock_minimo"])
        except ValueError:
            messagebox.showwarning("Error de formato", "Precio debe ser número, Stock y Stock mínimo deben ser enteros.")
            return

        # Guardar o actualizar
        try:
            if self.producto_id is None:
                InventarioController.guardar_producto(datos)
            else:
                InventarioController.actualizar_producto(self.producto_id, datos)
            messagebox.showinfo("Éxito", "Producto guardado correctamente.")
            self.ventana.destroy()
            if self.callback:
                self.callback()  # Refrescar tabla
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")