import tkinter as tk
from tkinter import messagebox

from controllers.login_controller import LoginController


class Login:

    def __init__(self):

        self.ventana = tk.Tk()

        self.ventana.title("Farmacia TPS")

        self.ventana.geometry("400x300")

        tk.Label(
            self.ventana,
            text="Usuario"
        ).pack(pady=10)

        self.usuario = tk.Entry(self.ventana)

        self.usuario.pack()

        tk.Label(
            self.ventana,
            text="Contraseña"
        ).pack(pady=10)

        self.password = tk.Entry(
            self.ventana,
            show="*"
        )

        self.password.pack()

        tk.Button(
            self.ventana,
            text="Ingresar",
            command=self.ingresar
        ).pack(pady=20)

        self.ventana.mainloop()

    def ingresar(self):

        usuario = self.usuario.get()

        password = self.password.get()

        datos = LoginController.autenticar(
            usuario,
            password
        )

        if datos is None:

            messagebox.showerror(
                "Error",
                "Credenciales incorrectas"
            )

            return

        messagebox.showinfo(
            "Bienvenido",
            f"Hola {datos['nombre']}\nRol: {datos['rol']}"
        )

        self.ventana.destroy()

        if datos["rol"] == "Administrador":

            from views.menu_admin import MenuAdmin

            MenuAdmin()

        else:

            from views.menu_empleado import MenuEmpleado

            MenuEmpleado()