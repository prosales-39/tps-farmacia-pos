import tkinter as tk
from datetime import datetime
from models.producto import Producto
from utils.helpers import formatear_precio

class DashboardView:

    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.cargar()

    def cargar(self):
        # Limpiar contenedor
        for widget in self.contenedor.winfo_children():
            widget.destroy()

        # Título
        tk.Label(
            self.contenedor,
            text="📊 Panel de Control",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#1565C0"
        ).pack(pady=(20, 10))

        tk.Label(
            self.contenedor,
            text="Resumen general del sistema",
            font=("Segoe UI", 12),
            bg="white",
            fg="#555"
        ).pack(pady=(0, 20))

        # Obtener datos reales
        productos = Producto.obtener_todos()
        total_productos = len(productos)
        stock_total = sum(p["stock"] for p in productos)
        valor_inventario = sum(p["precio"] * p["stock"] for p in productos)

        # Calcular productos por vencer (próximos 30 días)
        hoy = datetime.now().date()
        proximos_a_vencer = 0
        for p in productos:
            if p["fecha_vencimiento"]:
                try:
                    fecha_venc = datetime.strptime(p["fecha_vencimiento"], "%Y-%m-%d").date()
                    if (fecha_venc - hoy).days <= 30:
                        proximos_a_vencer += 1
                except:
                    pass

        # Tarjetas
        frame_tarjetas = tk.Frame(self.contenedor, bg="white")
        frame_tarjetas.pack(pady=10)

        tarjetas = [
            ("💊 Productos", total_productos, "#E3F2FD"),
            ("📦 Stock total", stock_total, "#FFF3E0"),
            ("💰 Valor inventario", formatear_precio(valor_inventario), "#E8F5E9"),
            ("⚠️ Próximos a vencer", proximos_a_vencer, "#FFEBEE")
        ]

        for i, (titulo, valor, color) in enumerate(tarjetas):
            frame = tk.Frame(frame_tarjetas, bg=color, width=220, height=120, relief="raised", bd=2)
            frame.grid(row=0, column=i, padx=10, pady=10)
            frame.pack_propagate(False)

            tk.Label(
                frame,
                text=titulo,
                font=("Segoe UI", 11),
                bg=color,
                fg="#333"
            ).pack(pady=(15, 5))

            tk.Label(
                frame,
                text=str(valor),
                font=("Segoe UI", 20, "bold"),
                bg=color,
                fg="#1565C0"
            ).pack()