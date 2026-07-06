import tkinter as tk
from views.inventario import InventarioView


class MainWindow:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Farmacia POS")

        self.root.geometry("1200x700")

        self.root.configure(bg="#ECECEC")

        self.crear_interfaz()

        self.root.mainloop()

    def limpiar_contenido(self):
        """Elimina el contenido del panel central."""

        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_inventario(self):
        """Carga el módulo de Inventario."""

        self.limpiar_contenido()

        InventarioView(self.contenido)

    def crear_interfaz(self):

        # ==========================
        # ENCABEZADO
        # ==========================

        header = tk.Frame(
            self.root,
            bg="#1565C0",
            height=60
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text="FARMACIA POS",
            bg="#1565C0",
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(side="left", padx=20)

        tk.Label(
            header,
            text="Administrador",
            bg="#1565C0",
            fg="white",
            font=("Segoe UI", 11)
        ).pack(side="right", padx=20)

        # ==========================
        # CONTENEDOR PRINCIPAL
        # ==========================

        principal = tk.Frame(self.root)

        principal.pack(fill="both", expand=True)

        # ==========================
        # MENÚ LATERAL
        # ==========================

        menu = tk.Frame(
            principal,
            width=220,
            bg="#263238"
        )

        menu.pack(side="left", fill="y")

        acciones = {
            "🏠 Inicio": lambda: None,
            "💊 Inventario": self.mostrar_inventario,
            "💰 Ventas": lambda: None,
            "🚚 Compras": lambda: None,
            "👥 Usuarios": lambda: None,
            "📦 Proveedores": lambda: None,
            "📊 Reportes": lambda: None,
            "🚪 Salir": self.root.destroy
        }

        for texto, accion in acciones.items():

            tk.Button(
                menu,
                text=texto,
                command=accion,
                relief="flat",
                bg="#263238",
                fg="white",
                activebackground="#37474F",
                activeforeground="white",
                font=("Segoe UI", 11),
                anchor="w",
                padx=20
            ).pack(fill="x", ipady=12)

        # ==========================
        # PANEL CENTRAL
        # ==========================

        self.contenido = tk.Frame(
            principal,
            bg="white"
        )

        self.contenido.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Mostrar Inventario por defecto
        self.mostrar_inventario()