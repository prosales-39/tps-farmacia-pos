import tkinter as tk
from tkinter import messagebox
from controllers.login_controller import LoginController
from views.main_window import MainWindow
import os

try:
    from PIL import Image, ImageTk
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("Pillow no instalado. Las imágenes se mostrarán sin redimensionar.")

class Login:

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("SaludPlus - Iniciar Sesión")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f2f5")

        self.crear_widgets()
        self.centrar_ventana()
        self.ventana.bind("<Return>", lambda event: self.ingresar())
        self.ventana.mainloop()

    def crear_widgets(self):
        self.logo_img = None
        ruta_logo = os.path.join("assets", "logo.png")

        logo_cargado = False
        if os.path.exists(ruta_logo):
            try:
                if PILLOW_AVAILABLE:
                    img = Image.open(ruta_logo)
                    img = img.resize((200, 100), Image.Resampling.LANCZOS)
                    self.logo_img = ImageTk.PhotoImage(img)
                else:
                    self.logo_img = tk.PhotoImage(file=ruta_logo)
                logo_cargado = True
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")

        if logo_cargado:
            lbl_logo = tk.Label(self.ventana, image=self.logo_img, bg="#f0f2f5")
            lbl_logo.pack(pady=(15, 5))
        else:
            tk.Label(
                self.ventana,
                text="🏥 SALUDPLUS",
                font=("Segoe UI", 26, "bold"),
                bg="#f0f2f5",
                fg="#1a237e"
            ).pack(pady=(20, 5))
            tk.Label(
                self.ventana,
                text="Sistema de Gestión Farmacéutica",
                font=("Segoe UI", 10),
                bg="#f0f2f5",
                fg="#666"
            ).pack(pady=(0, 10))

        tk.Label(
            self.ventana,
            text="Iniciar Sesión",
            font=("Segoe UI", 12),
            bg="#f0f2f5",
            fg="#555"
        ).pack(pady=(0, 20))

        frame = tk.Frame(self.ventana, bg="#f0f2f5")
        frame.pack(padx=40, fill="x")

        tk.Label(frame, text="Usuario:", font=("Segoe UI", 10), bg="#f0f2f5").pack(anchor="w")
        self.usuario = tk.Entry(
            frame,
            font=("Segoe UI", 11),
            bg="white",
            relief="flat",
            highlightthickness=1,
            highlightcolor="#1a237e"
        )
        self.usuario.pack(fill="x", pady=(5, 10), ipady=5)

        tk.Label(frame, text="Contraseña:", font=("Segoe UI", 10), bg="#f0f2f5").pack(anchor="w")
        self.password = tk.Entry(
            frame,
            show="*",
            font=("Segoe UI", 11),
            bg="white",
            relief="flat",
            highlightthickness=1,
            highlightcolor="#1a237e"
        )
        self.password.pack(fill="x", pady=(5, 15), ipady=5)

        btn_ingresar = tk.Button(
            frame,
            text="Ingresar",
            command=self.ingresar,
            bg="#1a237e",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        btn_ingresar.pack(pady=5)
        btn_ingresar.bind("<Enter>", lambda e: btn_ingresar.config(bg="#0d47a1"))
        btn_ingresar.bind("<Leave>", lambda e: btn_ingresar.config(bg="#1a237e"))

        self.ventana.geometry("420x450")

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = self.ventana.winfo_width()
        alto = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def ingresar(self):
        usuario = self.usuario.get().strip()
        password = self.password.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
            return

        datos = LoginController.autenticar(usuario, password)

        if datos is None:
            messagebox.showerror("Error", "Credenciales incorrectas")
            return

        # Convertir a dict y pasar a MainWindow
        datos_dict = dict(datos)
        self.ventana.destroy()
        MainWindow(datos_dict)