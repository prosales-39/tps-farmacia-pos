import tkinter as tk


class MenuAdmin:

    def __init__(self):

        ventana = tk.Tk()

        ventana.title("Administrador")

        ventana.geometry("700x500")

        tk.Label(
            ventana,
            text="MENÚ ADMINISTRADOR",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        botones = [
            "Inventario",
            "Ventas",
            "Compras",
            "Proveedores",
            "Usuarios",
            "Reportes",
            "Salir"
        ]

        for boton in botones:

            tk.Button(
                ventana,
                text=boton,
                width=30
            ).pack(pady=5)

        ventana.mainloop()