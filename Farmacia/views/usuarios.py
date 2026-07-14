import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuario_controller import UsuarioController
from views.formulario_usuario import FormularioUsuario

class UsuariosView:

    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.id_seleccionado = None
        self.crear_interfaz()
        self.cargar_tabla()

    def crear_interfaz(self):
        # Título
        tk.Label(
            self.contenedor,
            text="👥 Gestión de Usuarios",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#1565C0"
        ).pack(pady=(10, 5))

        # Frame para tabla
        frame_tabla = tk.Frame(self.contenedor, bg="white")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview
        columnas = ("ID", "Nombre", "Usuario", "Rol", "Estado")
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=18
        )

        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Usuario", text="Usuario")
        self.tabla.heading("Rol", text="Rol")
        self.tabla.heading("Estado", text="Estado")

        self.tabla.column("ID", width=50, anchor="center")
        self.tabla.column("Nombre", width=150, anchor="w")
        self.tabla.column("Usuario", width=120, anchor="w")
        self.tabla.column("Rol", width=100, anchor="center")
        self.tabla.column("Estado", width=80, anchor="center")

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.on_seleccionar)

        # Frame para botones
        frame_botones = tk.Frame(self.contenedor, bg="white")
        frame_botones.pack(fill="x", padx=20, pady=10)

        botones = [
            ("➕ Nuevo", self.nuevo_usuario),
            ("✏️ Editar", self.editar_usuario),
            ("🔴 Deshabilitar", self.deshabilitar_usuario),
            ("🟢 Habilitar", self.habilitar_usuario),
            ("🔄 Actualizar", self.cargar_tabla)
        ]

        for texto, comando in botones:
            tk.Button(
                frame_botones,
                text=texto,
                command=comando,
                relief="flat",
                bg="#E3F2FD",
                fg="#0D47A1",
                font=("Segoe UI", 10, "bold"),
                padx=15,
                pady=5
            ).pack(side="left", padx=(0, 10))

    def cargar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        usuarios = UsuarioController.listar_usuarios()
        for u in usuarios:
            estado_texto = "Activo" if u["estado"] == 1 else "Inactivo"
            self.tabla.insert(
                "",
                "end",
                values=(u["id"], u["nombre"], u["usuario"], u["rol"], estado_texto),
                tags=(u["id"],)
            )

    def on_seleccionar(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            self.id_seleccionado = item["tags"][0] if item["tags"] else None

    def nuevo_usuario(self):
        FormularioUsuario(
            parent=self.contenedor,
            callback=self.cargar_tabla
        )

    def editar_usuario(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Seleccionar", "Primero selecciona un usuario")
            return
        FormularioUsuario(
            parent=self.contenedor,
            usuario_id=self.id_seleccionado,
            callback=self.cargar_tabla
        )

    def deshabilitar_usuario(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Seleccionar", "Primero selecciona un usuario")
            return
        if messagebox.askyesno("Confirmar", "¿Deshabilitar este usuario?"):
            try:
                UsuarioController.deshabilitar_usuario(self.id_seleccionado)
                self.cargar_tabla()
                messagebox.showinfo("Éxito", "Usuario deshabilitado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo deshabilitar: {e}")

    def habilitar_usuario(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Seleccionar", "Primero selecciona un usuario")
            return
        if messagebox.askyesno("Confirmar", "¿Habilitar este usuario?"):
            try:
                UsuarioController.habilitar_usuario(self.id_seleccionado)
                self.cargar_tabla()
                messagebox.showinfo("Éxito", "Usuario habilitado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo habilitar: {e}")