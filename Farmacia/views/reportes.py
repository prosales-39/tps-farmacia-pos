import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from controllers.reportes_controller import ReportesController
from utils.helpers import formatear_precio

class ReportesView:

    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(
            self.contenedor,
            text="📊 Reportes",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#1565C0"
        ).pack(pady=(10, 5))

        self.notebook = ttk.Notebook(self.contenedor)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.crear_tab_ventas()
        self.crear_tab_stock()
        self.crear_tab_compras()
        self.crear_tab_usuarios()

        self.cargar_datos_ventas()
        self.cargar_datos_stock()
        self.cargar_datos_compras()
        self.cargar_datos_usuarios()

    def crear_tab_ventas(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💵 Ventas")

        frame_filtros = tk.Frame(tab, bg="white")
        frame_filtros.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_filtros, text="Desde:", bg="white").pack(side="left", padx=5)
        self.entry_fecha_ini = tk.Entry(frame_filtros, width=12)
        self.entry_fecha_ini.pack(side="left", padx=5)
        self.entry_fecha_ini.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))

        tk.Label(frame_filtros, text="Hasta:", bg="white").pack(side="left", padx=5)
        self.entry_fecha_fin = tk.Entry(frame_filtros, width=12)
        self.entry_fecha_fin.pack(side="left", padx=5)
        self.entry_fecha_fin.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Button(
            frame_filtros,
            text="Actualizar",
            command=self.cargar_datos_ventas,
            bg="#1565C0",
            fg="white",
            relief="flat"
        ).pack(side="left", padx=10)

        frame_botones_ventas = tk.Frame(tab, bg="white")
        frame_botones_ventas.pack(fill="x", padx=10, pady=5)
        
        tk.Button(
            frame_botones_ventas,
            text="📥 Exportar Excel",
            command=self.exportar_excel_ventas,
            bg="#1565C0",
            fg="white",
            relief="flat",
            padx=10
        ).pack(side="left", padx=5)

        frame_resultados = tk.Frame(tab, bg="white")
        frame_resultados.pack(fill="both", expand=True, padx=10, pady=10)

        self.frame_resumen_ventas = tk.Frame(frame_resultados, bg="white")
        self.frame_resumen_ventas.pack(fill="x", pady=5)

        tk.Label(frame_resultados, text="Productos más vendidos", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w")
        self.tree_top_productos = ttk.Treeview(
            frame_resultados,
            columns=("producto", "vendido", "ingresos"),
            show="headings",
            height=8
        )
        self.tree_top_productos.heading("producto", text="Producto")
        self.tree_top_productos.heading("vendido", text="Cantidad vendida")
        self.tree_top_productos.heading("ingresos", text="Ingresos")
        self.tree_top_productos.column("producto", width=250)
        self.tree_top_productos.column("vendido", width=100, anchor="center")
        self.tree_top_productos.column("ingresos", width=120, anchor="e")
        self.tree_top_productos.pack(fill="both", expand=True, pady=5)

    def crear_tab_stock(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📦 Inventario")

        frame_controles = tk.Frame(tab, bg="white")
        frame_controles.pack(fill="x", padx=10, pady=10)

        tk.Button(
            frame_controles,
            text="Actualizar",
            command=self.cargar_datos_stock,
            bg="#1565C0",
            fg="white",
            relief="flat"
        ).pack(side="left", padx=5)

        tk.Label(tab, text="⚠️ Productos con stock bajo", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", padx=10)
        self.tree_stock_bajo = ttk.Treeview(
            tab,
            columns=("codigo", "nombre", "stock", "minimo"),
            show="headings",
            height=8
        )
        self.tree_stock_bajo.heading("codigo", text="Código")
        self.tree_stock_bajo.heading("nombre", text="Producto")
        self.tree_stock_bajo.heading("stock", text="Stock actual")
        self.tree_stock_bajo.heading("minimo", text="Mínimo")
        self.tree_stock_bajo.column("codigo", width=80, anchor="center")
        self.tree_stock_bajo.column("nombre", width=200)
        self.tree_stock_bajo.column("stock", width=80, anchor="center")
        self.tree_stock_bajo.column("minimo", width=80, anchor="center")
        self.tree_stock_bajo.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(tab, text="⏳ Productos por vencer (próximos 30 días)", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", padx=10)
        self.tree_por_vencer = ttk.Treeview(
            tab,
            columns=("codigo", "nombre", "vencimiento", "stock"),
            show="headings",
            height=8
        )
        self.tree_por_vencer.heading("codigo", text="Código")
        self.tree_por_vencer.heading("nombre", text="Producto")
        self.tree_por_vencer.heading("vencimiento", text="Fecha vencimiento")
        self.tree_por_vencer.heading("stock", text="Stock")
        self.tree_por_vencer.column("codigo", width=80, anchor="center")
        self.tree_por_vencer.column("nombre", width=200)
        self.tree_por_vencer.column("vencimiento", width=120, anchor="center")
        self.tree_por_vencer.column("stock", width=80, anchor="center")
        self.tree_por_vencer.pack(fill="both", expand=True, padx=10, pady=5)

    def crear_tab_compras(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🚚 Compras")

        frame_filtros = tk.Frame(tab, bg="white")
        frame_filtros.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_filtros, text="Desde:", bg="white").pack(side="left", padx=5)
        self.entry_compra_ini = tk.Entry(frame_filtros, width=12)
        self.entry_compra_ini.pack(side="left", padx=5)
        self.entry_compra_ini.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))

        tk.Label(frame_filtros, text="Hasta:", bg="white").pack(side="left", padx=5)
        self.entry_compra_fin = tk.Entry(frame_filtros, width=12)
        self.entry_compra_fin.pack(side="left", padx=5)
        self.entry_compra_fin.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Button(
            frame_filtros,
            text="Actualizar",
            command=self.cargar_datos_compras,
            bg="#1565C0",
            fg="white",
            relief="flat"
        ).pack(side="left", padx=10)

        frame_botones_compras = tk.Frame(tab, bg="white")
        frame_botones_compras.pack(fill="x", padx=10, pady=5)

        tk.Button(
            frame_botones_compras,
            text="📥 Exportar Excel",
            command=self.exportar_excel_compras,
            bg="#1565C0",
            fg="white",
            relief="flat",
            padx=10
        ).pack(side="left", padx=5)

        self.frame_resumen_compras = tk.Frame(tab, bg="white")
        self.frame_resumen_compras.pack(fill="x", padx=10, pady=10)

        self.label_resumen_compras = tk.Label(tab, text="", font=("Segoe UI", 11), bg="white")
        self.label_resumen_compras.pack(padx=10, pady=10, anchor="w")

    def crear_tab_usuarios(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="👥 Usuarios")

        frame_controles = tk.Frame(tab, bg="white")
        frame_controles.pack(fill="x", padx=10, pady=10)

        tk.Button(
            frame_controles,
            text="Actualizar",
            command=self.cargar_datos_usuarios,
            bg="#1565C0",
            fg="white",
            relief="flat"
        ).pack(side="left", padx=5)

        tk.Button(
            frame_controles,
            text="📥 Exportar Excel",
            command=self.exportar_excel_usuarios,
            bg="#1565C0",
            fg="white",
            relief="flat",
            padx=10
        ).pack(side="left", padx=5)

        self.tree_ventas_por_usuario = ttk.Treeview(
            tab,
            columns=("usuario", "ventas", "ingresos"),
            show="headings",
            height=15
        )
        self.tree_ventas_por_usuario.heading("usuario", text="Usuario")
        self.tree_ventas_por_usuario.heading("ventas", text="Total ventas")
        self.tree_ventas_por_usuario.heading("ingresos", text="Ingresos generados")
        self.tree_ventas_por_usuario.column("usuario", width=150)
        self.tree_ventas_por_usuario.column("ventas", width=100, anchor="center")
        self.tree_ventas_por_usuario.column("ingresos", width=120, anchor="e")
        self.tree_ventas_por_usuario.pack(fill="both", expand=True, padx=10, pady=10)

    def cargar_datos_ventas(self):
        try:
            fecha_ini = self.entry_fecha_ini.get().strip()
            fecha_fin = self.entry_fecha_fin.get().strip()
            resumen = ReportesController.obtener_resumen_ventas(fecha_ini, fecha_fin)

            for widget in self.frame_resumen_ventas.winfo_children():
                widget.destroy()

            if resumen:
                total_ventas = resumen.get("total_ventas", 0)
                total_ingresos = resumen.get("total_ingresos", 0)
                promedio = resumen.get("promedio_venta", 0)
                total_iva = resumen.get("total_iva", 0)

                tk.Label(
                    self.frame_resumen_ventas,
                    text=f"Ventas: {total_ventas}",
                    font=("Segoe UI", 11, "bold"),
                    bg="white"
                ).pack(side="left", padx=15)

                tk.Label(
                    self.frame_resumen_ventas,
                    text=f"Ingresos: {formatear_precio(total_ingresos)}",
                    font=("Segoe UI", 11, "bold"),
                    bg="white",
                    fg="#1565C0"
                ).pack(side="left", padx=15)

                tk.Label(
                    self.frame_resumen_ventas,
                    text=f"Promedio: {formatear_precio(promedio)}",
                    font=("Segoe UI", 11),
                    bg="white"
                ).pack(side="left", padx=15)

                tk.Label(
                    self.frame_resumen_ventas,
                    text=f"IVA: {formatear_precio(total_iva)}",
                    font=("Segoe UI", 11),
                    bg="white"
                ).pack(side="left", padx=15)

            for item in self.tree_top_productos.get_children():
                self.tree_top_productos.delete(item)

            top = ReportesController.obtener_productos_mas_vendidos(5)
            for p in top:
                self.tree_top_productos.insert(
                    "",
                    "end",
                    values=(p["nombre"], p["total_vendido"], formatear_precio(p["total_ingresos"]))
                )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")

    def cargar_datos_stock(self):
        try:
            for item in self.tree_stock_bajo.get_children():
                self.tree_stock_bajo.delete(item)

            bajo = ReportesController.obtener_productos_stock_bajo()
            for p in bajo:
                self.tree_stock_bajo.insert(
                    "",
                    "end",
                    values=(p["codigo"], p["nombre"], p["stock"], p["stock_minimo"])
                )

            for item in self.tree_por_vencer.get_children():
                self.tree_por_vencer.delete(item)

            por_vencer = ReportesController.obtener_productos_por_vencer(30)
            for p in por_vencer:
                self.tree_por_vencer.insert(
                    "",
                    "end",
                    values=(p["codigo"], p["nombre"], p["fecha_vencimiento"], p["stock"])
                )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")

    def cargar_datos_compras(self):
        try:
            fecha_ini = self.entry_compra_ini.get().strip()
            fecha_fin = self.entry_compra_fin.get().strip()
            resumen = ReportesController.obtener_resumen_compras(fecha_ini, fecha_fin)

            if resumen:
                total_compras = resumen.get("total_compras", 0)
                total_gastado = resumen.get("total_gastado", 0)
                promedio = resumen.get("promedio_compra", 0)

                self.label_resumen_compras.config(
                    text=f"Compras: {total_compras} | Total gastado: {formatear_precio(total_gastado)} | Promedio: {formatear_precio(promedio)}"
                )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")

    def cargar_datos_usuarios(self):
        try:
            for item in self.tree_ventas_por_usuario.get_children():
                self.tree_ventas_por_usuario.delete(item)

            datos = ReportesController.obtener_ventas_por_usuario()
            for d in datos:
                self.tree_ventas_por_usuario.insert(
                    "",
                    "end",
                    values=(d["usuario"], d["total_ventas"], formatear_precio(d["total_ingresos"]))
                )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")

    def exportar_excel(self, datos, columnas, nombre_archivo="reporte"):
        import openpyxl
        from datetime import datetime
        from tkinter import filedialog
        
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("Todos los archivos", "*.*")],
            initialfile=f"{nombre_archivo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        
        if not archivo:
            return
            
        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Reporte"
            
            ws.append([col["titulo"] for col in columnas])
            
            for row in datos:
                ws.append([row.get(col["clave"], "") for col in columnas])
                
            wb.save(archivo)
            messagebox.showinfo("Exportación exitosa", f"Archivo guardado en:\n{archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

    def exportar_excel_ventas(self):
        try:
            fecha_ini = self.entry_fecha_ini.get().strip()
            fecha_fin = self.entry_fecha_fin.get().strip()
            
            resumen = ReportesController.obtener_resumen_ventas(fecha_ini, fecha_fin)
            top = ReportesController.obtener_productos_mas_vendidos(10)
            
            datos = []
            if resumen:
                datos.append({
                    "fecha": "RESUMEN",
                    "producto": "",
                    "cantidad": "",
                    "subtotal": resumen.get("subtotal", 0),
                    "iva": resumen.get("total_iva", 0),
                    "total": resumen.get("total_ingresos", 0)
                })
                
            for p in top:
                datos.append({
                    "fecha": "",
                    "producto": p["nombre"],
                    "cantidad": p["total_vendido"],
                    "subtotal": "",
                    "iva": "",
                    "total": p["total_ingresos"]
                })
                
            columnas = [
                {"titulo": "Fecha", "clave": "fecha"},
                {"titulo": "Producto", "clave": "producto"},
                {"titulo": "Cantidad", "clave": "cantidad"},
                {"titulo": "Subtotal", "clave": "subtotal"},
                {"titulo": "IVA", "clave": "iva"},
                {"titulo": "Total", "clave": "total"}
            ]
            
            self.exportar_excel(datos, columnas, "reporte_ventas")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

    def exportar_excel_compras(self):
        try:
            fecha_ini = self.entry_compra_ini.get().strip()
            fecha_fin = self.entry_compra_fin.get().strip()
            resumen = ReportesController.obtener_resumen_compras(fecha_ini, fecha_fin)
            
            datos = []
            if resumen:
                datos.append({
                    "compras": resumen.get("total_compras", 0),
                    "total_gastado": resumen.get("total_gastado", 0),
                    "promedio": resumen.get("promedio_compra", 0)
                })
                
            columnas = [
                {"titulo": "Total Compras", "clave": "compras"},
                {"titulo": "Total Gastado", "clave": "total_gastado"},
                {"titulo": "Promedio Compra", "clave": "promedio"}
            ]
            
            self.exportar_excel(datos, columnas, "reporte_compras")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

    def exportar_excel_usuarios(self):
        try:
            lista_usuarios = ReportesController.obtener_ventas_por_usuario()
            datos = []
            for d in lista_usuarios:
                datos.append({
                    "usuario": d["usuario"],
                    "ventas": d["total_ventas"],
                    "ingresos": d["total_ingresos"]
                })
                
            columnas = [
                {"titulo": "Usuario", "clave": "usuario"},
                {"titulo": "Total Ventas", "clave": "ventas"},
                {"titulo": "Ingresos Generados", "clave": "ingresos"}
            ]
            
            self.exportar_excel(datos, columnas, "reporte_usuarios")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")