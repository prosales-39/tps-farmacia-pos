import tkinter as tk
from views.dashboard import DashboardView
from views.inventario import InventarioView
from views.ventas import VentasView
from views.compras import ComprasView
from views.proveedores import ProveedoresView
from views.usuarios import UsuariosView
from views.reportes import ReportesView  # <--- DESCOMENTADO

class MainWindow:

    def __init__(self, usuario_data):
        self.usuario = usuario_data
        self.usuario_id = usuario_data["id"]
        self.root = tk.Tk()
        self.root.title("Farmacia POS")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ECECEC")

        self.crear_interfaz()
        self.root.mainloop()

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_dashboard(self):
        self.limpiar_contenido()
        DashboardView(self.contenido)

    def mostrar_inventario(self):
        self.limpiar_contenido()
        InventarioView(self.contenido)

    def mostrar_ventas(self):
        self.limpiar_contenido()
        VentasView(self.contenido, self.usuario_id)

    def mostrar_compras(self):
        self.limpiar_contenido()
        ComprasView(self.contenido, self.usuario_id)

    def mostrar_proveedores(self):
        self.limpiar_contenido()
        ProveedoresView(self.contenido)

    def mostrar_usuarios(self):
        self.limpiar_contenido()
        UsuariosView(self.contenido)

    def mostrar_reportes(self):
        self.limpiar_contenido()
        ReportesView(self.contenido)  # <--- AHORA USA LA VISTA REAL

    def mostrar_facturas(self):
        self.limpiar_contenido()
        from views.facturas import FacturasView
        FacturasView(self.contenido)

    def crear_interfaz(self):
        header = tk.Frame(self.root, bg="#1565C0", height=60)
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
            text=f"👤 {self.usuario['nombre']} ({self.usuario['rol']})",
            bg="#1565C0",
            fg="white",
            font=("Segoe UI", 11)
        ).pack(side="right", padx=20)

        principal = tk.Frame(self.root)
        principal.pack(fill="both", expand=True)

        menu = tk.Frame(principal, width=220, bg="#263238")
        menu.pack(side="left", fill="y")

        opciones = {
            "🏠 Inicio": self.mostrar_dashboard,
            "💊 Inventario": self.mostrar_inventario,
            "💰 Ventas": self.mostrar_ventas,
            "📄 Facturas": self.mostrar_facturas,
            "🚚 Compras": self.mostrar_compras,
            "👥 Usuarios": self.mostrar_usuarios,
            "📦 Proveedores": self.mostrar_proveedores,
            "📊 Reportes": self.mostrar_reportes,
            "🚪 Salir": self.root.destroy
        }

        for texto, comando in opciones.items():
            tk.Button(
                menu,
                text=texto,
                command=comando,
                relief="flat",
                bg="#263238",
                fg="white",
                activebackground="#37474F",
                activeforeground="white",
                font=("Segoe UI", 11),
                anchor="w",
                padx=20
            ).pack(fill="x", ipady=12)

        self.contenido = tk.Frame(principal, bg="white")
        self.contenido.pack(side="right", fill="both", expand=True)

        self.mostrar_dashboard()