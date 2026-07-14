import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuario_controller import UsuarioController

class FormularioUsuario:

    def __init__(self, parent, usuario_id=None, callback=None):
        self.parent = parent
        self.usuario_id = usuario_id
        self.callback = callback
        self.datos_iniciales = None

        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Nuevo Usuario" if not usuario_id else "Editar Usuario")
        self.ventana.geometry("450x400")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()

        self.crear_widgets()
        if usuario_id:
            self.cargar_datos()

    def crear_widgets(self):
        frame = tk.Frame(self.ventana, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Campos
        campos = [
            ("Nombre completo:", "nombre"),
            ("Usuario:", "usuario"),
            ("Contraseña:", "password")
        ]

        self.entries = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(frame, text=label, font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(frame, font=("Segoe UI", 10), width=30)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries[key] = entry

        # Para contraseña, mostramos asteriscos
        self.entries["password"].config(show="*")

        # Rol
        tk.Label(frame, text="Rol:", font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.combo_rol = ttk.Combobox(frame, state="readonly", width=27)
        self.combo_rol.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.cargar_roles()

        # Estado (solo visible en edición)
        self.estado_var = tk.IntVar(value=1)
        self.check_estado = tk.Checkbutton(
            frame,
            text="Activo",
            variable=self.estado_var,
            font=("Segoe UI", 10)
        )
        self.check_estado.grid(row=4, column=0, columnspan=2, pady=10, sticky="w")

        if not self.usuario_id:
            self.check_estado.grid_remove()  # Ocultar en nuevo

        # Botones
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

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

        # Si es edición, mostrar estado
        if self.usuario_id:
            self.check_estado.grid()

    def cargar_roles(self):
        roles = UsuarioController.obtener_roles()
        self.combo_rol["values"] = [r["nombre"] for r in roles]
        # Guardar mapeo id -> nombre para después
        self.roles_map = {r["nombre"]: r["id"] for r in roles}
        if roles:
            self.combo_rol.current(0)

    def cargar_datos(self):
        usuario = UsuarioController.obtener_usuario(self.usuario_id)
        if usuario:
            self.entries["nombre"].insert(0, usuario["nombre"])
            self.entries["usuario"].insert(0, usuario["usuario"])
            # Contraseña no se carga (se puede dejar en blanco para no cambiar)
            self.entries["password"].insert(0, "********")  # placeholder
            # Seleccionar rol
            rol_nombre = usuario["rol"]
            if rol_nombre in self.roles_map:
                self.combo_rol.set(rol_nombre)
            # Estado
            self.estado_var.set(usuario["estado"])
            self.check_estado.config(text="Activo" if usuario["estado"] == 1 else "Inactivo")
        else:
            messagebox.showerror("Error", "No se encontró el usuario")
            self.ventana.destroy()

    def guardar(self):
        nombre = self.entries["nombre"].get().strip()
        usuario = self.entries["usuario"].get().strip()
        password = self.entries["password"].get().strip()
        rol_nombre = self.combo_rol.get()
        estado = self.estado_var.get()

        if not nombre or not usuario:
            messagebox.showwarning("Campos incompletos", "Nombre y Usuario son obligatorios.")
            return

        if not self.usuario_id and not password:
            messagebox.showwarning("Campos incompletos", "La contraseña es obligatoria para usuarios nuevos.")
            return

        if not rol_nombre:
            messagebox.showwarning("Campos incompletos", "Seleccione un rol.")
            return

        rol_id = self.roles_map.get(rol_nombre)
        if not rol_id:
            messagebox.showerror("Error", "Rol no válido")
            return

        try:
            if self.usuario_id:
                # Edición: si la contraseña es "********" o vacía, no la actualizamos
                if password == "********" or password == "":
                    UsuarioController.actualizar_usuario(
                        self.usuario_id, nombre, usuario, None, rol_id, estado
                    )
                else:
                    UsuarioController.actualizar_usuario(
                        self.usuario_id, nombre, usuario, password, rol_id, estado
                    )
            else:
                UsuarioController.crear_usuario(nombre, usuario, password, rol_id)

            messagebox.showinfo("Éxito", "Usuario guardado correctamente.")
            self.ventana.destroy()
            if self.callback:
                self.callback()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")