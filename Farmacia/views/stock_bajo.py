import tkinter as tk
from tkinter import ttk
from models.notificacion import Notificacion
from utils.helpers import formatear_precio

class StockBajoView:

    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):
        tk.Label(
            self.contenedor,
            text="⚠️ Productos con Stock Bajo",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#D32F2F"
        ).pack(pady=(10, 5))

        frame_tabla = tk.Frame(self.contenedor, bg="white")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("Código", "Nombre", "Stock", "Mínimo", "Faltante")
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=18
        )

        self.tabla.heading("Código", text="Código")
        self.tabla.heading("Nombre", text="Producto")
        self.tabla.heading("Stock", text="Stock actual")
        self.tabla.heading("Mínimo", text="Mínimo")
        self.tabla.heading("Faltante", text="Faltante")

        self.tabla.column("Código", width=100, anchor="center")
        self.tabla.column("Nombre", width=250, anchor="w")
        self.tabla.column("Stock", width=100, anchor="center")
        self.tabla.column("Mínimo", width=100, anchor="center")
        self.tabla.column("Faltante", width=100, anchor="center")

        self.tabla.pack(fill="both", expand=True)

    def cargar_datos(self):
        productos = Notificacion.verificar_stock_bajo()
        
        for p in productos:
            self.tabla.insert(
                "",
                "end",
                values=(
                    p["codigo"],
                    p["nombre"],
                    p["stock"],
                    p["stock_minimo"],
                    p["faltante"]
                )
            )