import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from utils.backup import BackupManager
from utils.helpers import formatear_precio
from datetime import datetime
import os

class BackupView:

    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.crear_interfaz()
        self.cargar_backups()

    def crear_interfaz(self):
        tk.Label(
            self.contenedor,
            text="💾 Copias de Seguridad",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#1565C0"
        ).pack(pady=(10, 5))

        tk.Label(
            self.contenedor,
            text="Gestión de respaldos de la base de datos",
            font=("Segoe UI", 11),
            bg="white",
            fg="#555"
        ).pack(pady=(0, 10))

        # Frame de botones de acción
        frame_acciones = tk.Frame(self.contenedor, bg="white")
        frame_acciones.pack(fill="x", padx=20, pady=10)

        tk.Button(
            frame_acciones,
            text="📤 Crear Backup",
            command=self.crear_backup,
            bg="#43A047",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=20,
            pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            frame_acciones,
            text="📥 Restaurar Backup",
            command=self.restaurar_backup,
            bg="#1565C0",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=20,
            pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            frame_acciones,
            text="🗑️ Limpiar Antiguos",
            command=self.limpiar_antiguos,
            bg="#E53935",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=20,
            pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            frame_acciones,
            text="🔄 Actualizar",
            command=self.cargar_backups,
            bg="#78909C",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=20,
            pady=8
        ).pack(side="left", padx=5)

        # Frame para tabla de backups
        frame_tabla = tk.Frame(self.contenedor, bg="white")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal")

        columnas = ("Nombre", "Fecha", "Tamaño", "Acciones")
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=15
        )

        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        self.tabla.heading("Nombre", text="Archivo")
        self.tabla.heading("Fecha", text="Fecha de creación")
        self.tabla.heading("Tamaño", text="Tamaño")
        self.tabla.heading("Acciones", text="Acciones")

        self.tabla.column("Nombre", width=250, anchor="w")
        self.tabla.column("Fecha", width=180, anchor="center")
        self.tabla.column("Tamaño", width=100, anchor="e")
        self.tabla.column("Acciones", width=150, anchor="center")

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # Label de información
        self.label_info = tk.Label(
            self.contenedor,
            text="",
            font=("Segoe UI", 10),
            bg="white",
            fg="#666"
        )
        self.label_info.pack(pady=5)

    def cargar_backups(self):
        """Carga la lista de backups en la tabla."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        backups = BackupManager.listar_backups()

        if not backups:
            self.label_info.config(text="No hay copias de seguridad disponibles.")
            return

        self.label_info.config(text=f"Total: {len(backups)} copia(s) de seguridad")

        for backup in backups:
            # Formatear tamaño
            tamaño = backup["tamaño"]
            if tamaño < 1024:
                tamaño_str = f"{tamaño} B"
            elif tamaño < 1024 * 1024:
                tamaño_str = f"{tamaño / 1024:.1f} KB"
            else:
                tamaño_str = f"{tamaño / (1024 * 1024):.1f} MB"

            fecha_str = backup["fecha"].strftime("%d/%m/%Y %H:%M:%S")

            # Insertar en tabla
            item_id = self.tabla.insert(
                "",
                "end",
                values=(backup["nombre"], fecha_str, tamaño_str, "⬇️ Restaurar | ❌ Eliminar")
            )

            # Guardar ruta en tags para acciones
            self.tabla.item(item_id, tags=(str(backup["ruta"]),))

    def crear_backup(self):
        """Crea una nueva copia de seguridad."""
        try:
            backup_path = BackupManager.crear_backup()
            
            # Limpiar backups antiguos (mantener 10)
            eliminados = BackupManager.limpiar_backups_antiguos(10)
            
            mensaje = f"✅ Backup creado exitosamente:\n{backup_path}"
            if eliminados > 0:
                mensaje += f"\n\n🗑️ {eliminados} backup(s) antiguo(s) eliminado(s)"
            
            messagebox.showinfo("Backup exitoso", mensaje)
            self.cargar_backups()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el backup:\n{str(e)}")

    def restaurar_backup(self):
        """Restaura una copia de seguridad seleccionada."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Seleccionar", "Primero seleccione un backup.")
            return

        # Obtener ruta del backup
        item = self.tabla.item(seleccion[0])
        backup_path = item["tags"][0]

        if not messagebox.askyesno(
            "Confirmar restauración",
            "⚠️ ADVERTENCIA: Esto sobrescribirá la base de datos actual.\n"
            "Se creará un backup automático antes de restaurar.\n\n"
            f"¿Restaurar backup: {item['values'][0]}?"
        ):
            return

        try:
            BackupManager.restaurar_backup(backup_path)
            messagebox.showinfo(
                "Restauración exitosa",
                "✅ Base de datos restaurada correctamente.\n"
                "Se creó un backup de la base de datos anterior."
            )
            self.cargar_backups()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo restaurar:\n{str(e)}")

    def limpiar_antiguos(self):
        """Elimina backups antiguos (mantiene los 5 más recientes)."""
        if not messagebox.askyesno(
            "Confirmar limpieza",
            "⚠️ ¿Eliminar backups antiguos?\n"
            "Se mantendrán los 5 más recientes."
        ):
            return

        try:
            eliminados = BackupManager.limpiar_backups_antiguos(5)
            if eliminados > 0:
                messagebox.showinfo("Limpieza completada", f"🗑️ {eliminados} backup(s) eliminado(s).")
            else:
                messagebox.showinfo("Limpieza completada", "No hay backups antiguos para eliminar.")
            self.cargar_backups()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo limpiar:\n{str(e)}")