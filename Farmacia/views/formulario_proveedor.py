import tkinter as tk
from tkinter import messagebox

class FormularioProveedor:

    def __init__(self, parent, proveedor_id=None, callback_guardar=None):
        self.parent = parent
        self.proveedor_id = proveedor_id
        self.callback = callback_guardar

        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Nuevo Proveedor" if proveedor_id is None else "Editar Proveedor")
        self.ventana.geometry("450x350")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()

        self.crear_widgets()

        if proveedor_id:
            self.cargar_datos()

    def crear_widgets(self):
        frame = tk.Frame(self.ventana, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        campos = [
            ("Nombre:", "nombre"),
            ("Teléfono:", "telefono"),
            ("Correo:", "correo"),
            ("Dirección:", "direccion"),
        ]

        self.entries = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(frame, text=label, font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(frame, font=("Segoe UI", 10), width=30)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries[key] = entry

        # Botones
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)

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
        from controllers.proveedores_controller import ProveedoresController
        proveedor = ProveedoresController.obtener_proveedor(self.proveedor_id)
        if proveedor:
            self.entries["nombre"].insert(0, proveedor["nombre"])
            self.entries["telefono"].insert(0, proveedor["telefono"] or "")
            self.entries["correo"].insert(0, proveedor["correo"] or "")
            self.entries["direccion"].insert(0, proveedor["direccion"] or "")
        else:
            messagebox.showerror("Error", "No se encontró el proveedor.")
            self.ventana.destroy()

    def guardar(self):
        datos = {
            "nombre": self.entries["nombre"].get().strip(),
            "telefono": self.entries["telefono"].get().strip(),
            "correo": self.entries["correo"].get().strip(),
            "direccion": self.entries["direccion"].get().strip()
        }

        if not datos["nombre"]:
            messagebox.showwarning("Campos incompletos", "El nombre es obligatorio.")
            return

        from controllers.proveedores_controller import ProveedoresController
        try:
            if self.proveedor_id is None:
                ProveedoresController.guardar_proveedor(datos)
            else:
                ProveedoresController.actualizar_proveedor(self.proveedor_id, datos)
            messagebox.showinfo("Éxito", "Proveedor guardado correctamente.")
            self.ventana.destroy()
            if self.callback:
                self.callback()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")