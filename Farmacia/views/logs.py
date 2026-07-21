import tkinter as tk
from tkinter import ttk, messagebox
from utils.logger import Logger
from datetime import datetime

class LogsView:

    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.crear_interfaz()
        self.cargar_logs()

    def crear_interfaz(self):
        tk.Label(
            self.contenedor,
            text="📋 Registro de Actividades (Logs)",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#1565C0"
        ).pack(pady=(10, 5))

        tk.Label(
            self.contenedor,
            text="Historial de acciones del sistema",
            font=("Segoe UI", 11),
            bg="white",
            fg="#555"
        ).pack(pady=(0, 10))

        # Frame para botones
        frame_botones = tk.Frame(self.contenedor, bg="white")
        frame_botones.pack(fill="x", padx=20, pady=5)

        tk.Button(
            frame_botones,
            text="🔄 Actualizar",
            command=self.cargar_logs,
            bg="#1565C0",
            fg="white",
            relief="flat",
            padx=15
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botones,
            text="📤 Exportar Logs",
            command=self.exportar_logs,
            bg="#43A047",
            fg="white",
            relief="flat",
            padx=15
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botones,
            text="🗑️ Limpiar Logs",
            command=self.limpiar_logs,
            bg="#E53935",
            fg="white",
            relief="flat",
            padx=15
        ).pack(side="left", padx=5)

        # Frame para tabla
        frame_tabla = tk.Frame(self.contenedor, bg="white")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal")

        columnas = ("Fecha", "Nivel", "Mensaje")
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=20
        )

        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        self.tabla.heading("Fecha", text="Fecha y Hora")
        self.tabla.heading("Nivel", text="Nivel")
        self.tabla.heading("Mensaje", text="Mensaje")

        self.tabla.column("Fecha", width=180, anchor="center")
        self.tabla.column("Nivel", width=100, anchor="center")
        self.tabla.column("Mensaje", width=500, anchor="w")

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # Configurar colores por nivel
        self.tabla.tag_configure("INFO", foreground="green")
        self.tabla.tag_configure("WARNING", foreground="orange")
        self.tabla.tag_configure("ERROR", foreground="red")

    def cargar_logs(self):
        """Carga los logs en la tabla."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        logs = Logger.obtener_logs(200)

        for log in logs:
            # Parsear la línea de log
            try:
                partes = log.strip().split(" - ", 2)
                if len(partes) >= 3:
                    fecha = partes[0]
                    nivel = partes[1]
                    mensaje = partes[2]
                    self.tabla.insert(
                        "",
                        "end",
                        values=(fecha, nivel, mensaje),
                        tags=(nivel,)
                    )
            except:
                pass

    def exportar_logs(self):
        """Exporta los logs a un archivo de texto."""
        from tkinter import filedialog
        from datetime import datetime

        archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")],
            initialfile=f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        if not archivo:
            return

        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("REGISTRO DE ACTIVIDADES - FARMACIA POS\n")
                f.write(f"Exportado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")

                logs = Logger.obtener_logs(500)
                for log in logs:
                    f.write(log)

            messagebox.showinfo("Éxito", f"Logs exportados a:\n{archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

    def limpiar_logs(self):
        """Limpia el archivo de logs."""
        if not messagebox.askyesno("Confirmar", "¿Eliminar todos los logs?"):
            return

        try:
            from pathlib import Path
            log_path = Path("logs") / "farmacia.log"
            if log_path.exists():
                with open(log_path, 'w', encoding='utf-8') as f:
                    f.write("")
                self.cargar_logs()
                messagebox.showinfo("Éxito", "Logs limpiados correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo limpiar: {e}")