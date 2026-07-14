import tkinter as tk
from tkinter import ttk, messagebox
from controllers.proveedores_controller import ProveedoresController
from views.formulario_proveedor import FormularioProveedor

class ProveedoresView:

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

        columnas = ("Nombre", "Teléfono", "Correo", "Dirección")
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

        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Teléfono", text="Teléfono")
        self.tabla.heading("Correo", text="Correo")
        self.tabla.heading("Dirección", text="Dirección")

        self.tabla.column("Nombre", width=150, anchor="w")
        self.tabla.column("Teléfono", width=120, anchor="center")
        self.tabla.column("Correo", width=180, anchor="w")
        self.tabla.column("Dirección", width=180, anchor="w")

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
            ("➕ Nuevo", self.nuevo_proveedor),
            ("✏️ Editar", self.editar_proveedor),
            ("🗑️ Eliminar", self.eliminar_proveedor),
            ("🔄 Actualizar", self.cargar_tabla)
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

    def cargar_tabla(self, proveedores=None):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        if proveedores is None:
            proveedores = ProveedoresController.listar_proveedores()

        for p in proveedores:
            self.tabla.insert(
                "",
                "end",
                values=(
                    p["nombre"],
                    p["telefono"] or "",
                    p["correo"] or "",
                    p["direccion"] or ""
                ),
                tags=(p["id"],)
            )

    def buscar_automatico(self, event=None):
        termino = self.entry_busqueda.get().strip()
        if termino:
            proveedores = ProveedoresController.buscar_proveedores(termino)
        else:
            proveedores = ProveedoresController.listar_proveedores()
        self.cargar_tabla(proveedores)

    def limpiar_busqueda(self):
        self.entry_busqueda.delete(0, tk.END)
        self.cargar_tabla()

    def on_seleccionar(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            self.id_seleccionado = item["tags"][0] if item["tags"] else None

    def nuevo_proveedor(self):
        FormularioProveedor(
            self.contenedor,
            proveedor_id=None,
            callback_guardar=self.cargar_tabla
        )

    def editar_proveedor(self):
        if self.id_seleccionado:
            FormularioProveedor(
                self.contenedor,
                proveedor_id=self.id_seleccionado,
                callback_guardar=self.cargar_tabla
            )
        else:
            messagebox.showwarning("Seleccionar", "Primero selecciona un proveedor")

    def eliminar_proveedor(self):
        if self.id_seleccionado:
            if messagebox.askyesno("Confirmar", "¿Eliminar este proveedor?"):
                try:
                    ProveedoresController.eliminar_proveedor(self.id_seleccionado)
                    self.cargar_tabla()
                    self.id_seleccionado = None
                    messagebox.showinfo("Eliminado", "Proveedor eliminado correctamente.")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
        else:
            messagebox.showwarning("Seleccionar", "Primero selecciona un proveedor")