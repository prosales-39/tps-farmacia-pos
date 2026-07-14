import tkinter as tk
from tkinter import messagebox
from controllers.login_controller import LoginController
from views.main_window import MainWindow
from views.ventas import VentasView
from views.compras import ComprasView



class Login:

    def __init__(self):

        self.ventana = tk.Tk()
        self.ventana.title("Farmacia TPS")
        self.ventana.geometry("400x300")
        self.ventana.resizable(False, False)

        tk.Label(
            self.ventana,
            text="FARMACIA POS",
            font=("Segoe UI", 20, "bold"),
            fg="#1565C0"
        ).pack(pady=(30, 10))

        tk.Label(
            self.ventana,
            text="Iniciar Sesión",
            font=("Segoe UI", 12),
            fg="#333"
        ).pack(pady=(0, 20))

        frame = tk.Frame(self.ventana)
        frame.pack(padx=40, fill="x")

        tk.Label(frame, text="Usuario:", font=("Segoe UI", 10)).pack(anchor="w")
        self.usuario = tk.Entry(frame, font=("Segoe UI", 11))
        self.usuario.pack(fill="x", pady=(5, 10))

        tk.Label(frame, text="Contraseña:", font=("Segoe UI", 10)).pack(anchor="w")
        self.password = tk.Entry(frame, show="*", font=("Segoe UI", 11))
        self.password.pack(fill="x", pady=(5, 15))

        tk.Button(
            frame,
            text="Ingresar",
            command=self.ingresar,
            bg="#1565C0",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=20,
            pady=8
        ).pack(pady=5)

        tk.Label(
            self.ventana,
            text="Usuario: admin  |  Contraseña: admin123",
            font=("Segoe UI", 9),
            fg="#888"
        ).pack(pady=10)

        self.ventana.mainloop()

    def ingresar(self):

        usuario = self.usuario.get()
        password = self.password.get()

        if not usuario or not password:
            messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
            return

        datos = LoginController.autenticar(usuario, password)

        if datos is None:
            messagebox.showerror("Error", "Credenciales incorrectas")
            return

        self.ventana.destroy()
        # Abrir la ventana principal con los datos del usuario
        MainWindow(dict(datos))  # Convertir Row a dict