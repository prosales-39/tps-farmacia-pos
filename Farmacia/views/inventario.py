import tkinter as tk
from tkinter import ttk


class InventarioView:

    def __init__(self, parent):

        titulo = tk.Label(
            parent,
            text="Inventario",
            bg="white",
            font=("Segoe UI", 20, "bold")
        )

        titulo.pack(pady=20)

        barra = tk.Frame(parent, bg="white")
        barra.pack(fill="x", padx=20)

        tk.Label(
            barra,
            text="Buscar:",
            bg="white"
        ).pack(side="left")

        tk.Entry(
            barra,
            width=40
        ).pack(side="left", padx=10)

        tk.Button(
            barra,
            text="Buscar"
        ).pack(side="left")

        columnas = (
            "codigo",
            "nombre",
            "stock",
            "precio",
            "vence",
            "lote"
        )

        tabla = ttk.Treeview(
            parent,
            columns=columnas,
            show="headings",
            height=18
        )

        for columna, texto in zip(
            columnas,
            ["Código", "Medicamento", "Stock", "Precio", "Vencimiento", "Lote"]
        ):
            tabla.heading(columna, text=texto)

        tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        botones = tk.Frame(parent, bg="white")
        botones.pack(pady=15)

        for texto in (
            "Nuevo",
            "Editar",
            "Eliminar",
            "Actualizar"
        ):

            tk.Button(
                botones,
                text=texto,
                width=14
            ).pack(side="left", padx=8)