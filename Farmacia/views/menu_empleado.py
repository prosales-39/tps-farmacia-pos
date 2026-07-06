import tkinter as tk


class MenuEmpleado:

    def __init__(self):

        ventana = tk.Tk()

        ventana.title("Empleado")

        ventana.geometry("700x500")

        tk.Label(
            ventana,
            text="MENÚ EMPLEADO",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        botones = [
            "Ventas",
            "Consultar Inventario",
            "Registrar Receta",
            "Salir"
        ]

        for boton in botones:

            tk.Button(
                ventana,
                text=boton,
                width=30
            ).pack(pady=5)

        ventana.mainloop()