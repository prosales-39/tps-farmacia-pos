import tkinter as tk
from tkinter import ttk, messagebox
from controllers.ventas_controller import VentasController
from utils.helpers import formatear_precio
from database.conexion import get_connection

class VentasView:

    def __init__(self, contenedor, usuario_id):
        self.contenedor = contenedor
        self.usuario_id = usuario_id
        self.carrito = []
        self.total = 0.0
        self.cliente_seleccionado = None

        self.crear_interfaz()
        self.buscar_productos()
        self.cargar_cliente_mostrador()

    def crear_interfaz(self):
        # Título
        tk.Label(
            self.contenedor,
            text="💰 Ventas",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#1565C0"
        ).pack(pady=(10, 5))

        # Frame para selección de cliente
        frame_cliente = tk.Frame(self.contenedor, bg="white")
        frame_cliente.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_cliente, text="Buscar cliente:", bg="white", font=("Segoe UI", 11)).pack(side="left", padx=5)
        
        self.entry_buscar_cliente = tk.Entry(frame_cliente, font=("Segoe UI", 11), width=25)
        self.entry_buscar_cliente.pack(side="left", padx=5)
        self.entry_buscar_cliente.bind("<KeyRelease>", self.buscar_clientes_automatico)

        tk.Button(
            frame_cliente,
            text="🔍 Buscar",
            command=self.buscar_clientes_automatico,
            bg="#1565C0",
            fg="white",
            relief="flat",
            padx=10
        ).pack(side="left", padx=5)

        tk.Button(
            frame_cliente,
            text="➕ Nuevo Cliente",
            command=self.nuevo_cliente,
            bg="#43A047",
            fg="white",
            relief="flat",
            padx=10
        ).pack(side="left", padx=5)

        tk.Button(
            frame_cliente,
            text="📋 Historial",
            command=self.ver_historial_cliente,
            bg="#1565C0",
            fg="white",
            relief="flat",
            padx=10
        ).pack(side="left", padx=5)

        # Label para mostrar cliente seleccionado
        self.label_cliente_seleccionado = tk.Label(
            frame_cliente,
            text="Cliente: Mostrador",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#1565C0"
        )
        self.label_cliente_seleccionado.pack(side="right", padx=10)

        # Lista de resultados de búsqueda
        self.frame_resultados = tk.Frame(self.contenedor, bg="white", height=100)
        self.frame_resultados.pack(fill="x", padx=20, pady=5)
        self.frame_resultados.pack_propagate(False)
        self.frame_resultados.pack_forget()

        # Treeview para resultados de clientes
        self.tree_clientes = ttk.Treeview(
            self.frame_resultados,
            columns=("id", "documento", "nombre", "telefono"),
            show="headings",
            height=4
        )
        self.tree_clientes.heading("id", text="ID")
        self.tree_clientes.heading("documento", text="Documento")
        self.tree_clientes.heading("nombre", text="Nombre")
        self.tree_clientes.heading("telefono", text="Teléfono")
        self.tree_clientes.column("id", width=40, anchor="center")
        self.tree_clientes.column("documento", width=120, anchor="center")
        self.tree_clientes.column("nombre", width=200, anchor="w")
        self.tree_clientes.column("telefono", width=120, anchor="center")

        scroll_clientes = ttk.Scrollbar(self.frame_resultados, orient="vertical", command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscrollcommand=scroll_clientes.set)

        self.tree_clientes.pack(side="left", fill="both", expand=True)
        scroll_clientes.pack(side="right", fill="y")

        self.tree_clientes.bind("<<TreeviewSelect>>", self.on_cliente_seleccionado)
        self.tree_clientes.bind("<Double-1>", self.on_cliente_doble_click)

        # Panel principal
        panel_principal = tk.Frame(self.contenedor, bg="white")
        panel_principal.pack(fill="both", expand=True, padx=10, pady=5)

        # --- Panel izquierdo ---
        panel_izq = tk.Frame(panel_principal, bg="white", width=500)
        panel_izq.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Búsqueda
        frame_buscar = tk.Frame(panel_izq, bg="white")
        frame_buscar.pack(fill="x", pady=5)
        tk.Label(frame_buscar, text="Buscar producto:", bg="white").pack(side="left", padx=5)
        self.entry_busqueda = tk.Entry(frame_buscar, width=30)
        self.entry_busqueda.pack(side="left", padx=5)
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self.buscar_productos())
        tk.Button(
            frame_buscar,
            text="Buscar",
            command=self.buscar_productos,
            bg="#1565C0",
            fg="white",
            relief="flat"
        ).pack(side="left", padx=5)

        # Treeview de productos disponibles
        self.tree_productos = ttk.Treeview(
            panel_izq,
            columns=("codigo", "nombre", "stock", "precio"),
            show="headings",
            height=15
        )
        self.tree_productos.heading("codigo", text="Código")
        self.tree_productos.heading("nombre", text="Producto")
        self.tree_productos.heading("stock", text="Stock")
        self.tree_productos.heading("precio", text="Precio")
        self.tree_productos.column("codigo", width=80)
        self.tree_productos.column("nombre", width=180)
        self.tree_productos.column("stock", width=60)
        self.tree_productos.column("precio", width=80)
        self.tree_productos.pack(fill="both", expand=True, pady=5)

        # Botón agregar al carrito
        btn_agregar = tk.Button(
            panel_izq,
            text="Agregar al carrito",
            command=self.agregar_al_carrito,
            bg="#43A047",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )
        btn_agregar.pack(pady=5)

        # --- Panel derecho (carrito) ---
        panel_der = tk.Frame(panel_principal, bg="white", width=400)
        panel_der.pack(side="right", fill="both", expand=True, padx=(5, 0))
        panel_der.pack_propagate(False)
        panel_der.config(width=400)

        tk.Label(panel_der, text="Carrito de venta", font=("Segoe UI", 12, "bold"), bg="white").pack(pady=5)

        self.tree_carrito = ttk.Treeview(
            panel_der,
            columns=("producto", "cantidad", "precio", "subtotal"),
            show="headings",
            height=12
        )
        self.tree_carrito.heading("producto", text="Producto")
        self.tree_carrito.heading("cantidad", text="Cant.")
        self.tree_carrito.heading("precio", text="Precio")
        self.tree_carrito.heading("subtotal", text="Subtotal")
        self.tree_carrito.column("producto", width=120)
        self.tree_carrito.column("cantidad", width=60)
        self.tree_carrito.column("precio", width=80)
        self.tree_carrito.column("subtotal", width=80)
        self.tree_carrito.pack(fill="both", expand=True, pady=5)

        # Botón eliminar
        btn_eliminar = tk.Button(
            panel_der,
            text="Eliminar seleccionado",
            command=self.eliminar_del_carrito,
            bg="#E53935",
            fg="white",
            relief="flat"
        )
        btn_eliminar.pack(pady=5)

        # Botón finalizar venta
        btn_finalizar = tk.Button(
            panel_der,
            text="Finalizar venta",
            command=self.finalizar_venta,
            bg="#1565C0",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            padx=20,
            pady=8
        )
        btn_finalizar.pack(pady=10)

        # Totales
        frame_totales = tk.Frame(panel_der, bg="white")
        frame_totales.pack(fill="x", pady=10)

        self.label_subtotal = tk.Label(frame_totales, text="Subtotal: $0", font=("Segoe UI", 11), bg="white")
        self.label_subtotal.pack(anchor="e")

        self.label_total = tk.Label(frame_totales, text="Total: $0", font=("Segoe UI", 14, "bold"), fg="#1565C0", bg="white")
        self.label_total.pack(anchor="e")

    def cargar_cliente_mostrador(self):
        """Carga el cliente Mostrador por defecto."""
        from models.cliente import Cliente
        clientes = Cliente.obtener_todos()
        for c in clientes:
            if c["nombre"] == "Mostrador":
                self.cliente_seleccionado = c["id"]
                self.label_cliente_seleccionado.config(text=f"Cliente: {c['nombre']} ({c['documento']})")
                return
        
        if clientes:
            self.cliente_seleccionado = clientes[0]["id"]
            self.label_cliente_seleccionado.config(text=f"Cliente: {clientes[0]['nombre']}")

    def buscar_clientes_automatico(self, event=None):
        """Busca clientes por documento o nombre."""
        from models.cliente import Cliente
        termino = self.entry_buscar_cliente.get().strip()
        
        if not termino:
            self.frame_resultados.pack_forget()
            return
        
        self.frame_resultados.pack(fill="x", padx=20, pady=5)
        
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        clientes = Cliente.buscar(termino)
        
        if not clientes:
            self.tree_clientes.insert("", "end", values=("", "", "No se encontraron clientes", ""))
            return
        
        for c in clientes:
            self.tree_clientes.insert(
                "",
                "end",
                values=(c["id"], c["documento"] or "", c["nombre"], c["telefono"] or "")
            )

    def on_cliente_seleccionado(self, event):
        """Selecciona un cliente de la lista."""
        seleccion = self.tree_clientes.selection()
        if not seleccion:
            return
        
        item = self.tree_clientes.item(seleccion[0])
        valores = item["values"]
        if not valores or not valores[0]:
            return
        
        cliente_id = valores[0]
        self.cliente_seleccionado = cliente_id
        
        from models.cliente import Cliente
        cliente = Cliente.obtener_por_id(cliente_id)
        if cliente:
            self.label_cliente_seleccionado.config(
                text=f"Cliente: {cliente['nombre']} ({cliente['documento']})"
            )
        
        self.frame_resultados.pack_forget()
        self.entry_buscar_cliente.delete(0, tk.END)

    def on_cliente_doble_click(self, event):
        """Selecciona cliente al hacer doble clic."""
        self.on_cliente_seleccionado(event)

    def nuevo_cliente(self):
        """Abre una ventana para crear un nuevo cliente."""
        ventana = tk.Toplevel(self.contenedor)
        ventana.title("Nuevo Cliente")
        ventana.geometry("400x300")
        ventana.resizable(False, False)
        ventana.grab_set()

        frame = tk.Frame(ventana, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        campos = [
            ("Documento:", "documento"),
            ("Nombre completo:", "nombre"),
            ("Teléfono:", "telefono"),
            ("Dirección:", "direccion")
        ]

        entries = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(frame, text=label, font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(frame, font=("Segoe UI", 10), width=30)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entries[key] = entry

        def guardar_cliente():
            from models.cliente import Cliente
            documento = entries["documento"].get().strip()
            nombre = entries["nombre"].get().strip()
            telefono = entries["telefono"].get().strip()
            direccion = entries["direccion"].get().strip()

            if not documento or not nombre:
                messagebox.showwarning("Campos incompletos", "Documento y nombre son obligatorios.")
                return

            try:
                Cliente.crear(documento, nombre, telefono, direccion)
                messagebox.showinfo("Éxito", "Cliente creado correctamente.")
                ventana.destroy()
                self.cargar_cliente_mostrador()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el cliente: {e}")

        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)

        tk.Button(
            btn_frame,
            text="Guardar",
            command=guardar_cliente,
            bg="#1565C0",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=5
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Cancelar",
            command=ventana.destroy,
            bg="#78909C",
            fg="white",
            font=("Segoe UI", 10),
            relief="flat",
            padx=20,
            pady=5
        ).pack(side="left", padx=10)

    def ver_historial_cliente(self):
        """Abre una ventana con el historial de compras del cliente seleccionado."""
        if not self.cliente_seleccionado:
            messagebox.showwarning("Seleccionar", "Primero seleccione un cliente.")
            return

        from models.cliente import Cliente
        cliente = Cliente.obtener_por_id(self.cliente_seleccionado)
        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado.")
            return

        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                v.id,
                v.fecha,
                v.total,
                COUNT(dv.id) as productos,
                GROUP_CONCAT(p.nombre, ', ') as productos_nombres
            FROM ventas v
            INNER JOIN detalle_venta dv ON v.id = dv.venta_id
            INNER JOIN productos p ON dv.producto_id = p.id
            WHERE v.cliente_id = ?
            GROUP BY v.id
            ORDER BY v.fecha DESC
            LIMIT 20
        """, (self.cliente_seleccionado,))
        historial = cursor.fetchall()
        conexion.close()

        ventana = tk.Toplevel(self.contenedor)
        ventana.title(f"Historial de {cliente['nombre']}")
        ventana.geometry("800x500")
        ventana.grab_set()

        tk.Label(
            ventana,
            text=f"📋 Historial de compras - {cliente['nombre']}",
            font=("Segoe UI", 16, "bold"),
            bg="white",
            fg="#1565C0"
        ).pack(pady=10)

        if not historial:
            tk.Label(
                ventana,
                text="Este cliente no tiene compras registradas.",
                font=("Segoe UI", 12),
                bg="white",
                fg="#555"
            ).pack(pady=50)
            return

        frame_tabla = tk.Frame(ventana, bg="white")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("Fecha", "Total", "Productos", "Detalle")
        tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=15
        )

        tabla.heading("Fecha", text="Fecha")
        tabla.heading("Total", text="Total")
        tabla.heading("Productos", text="Cant. Productos")
        tabla.heading("Detalle", text="Productos")

        tabla.column("Fecha", width=120, anchor="center")
        tabla.column("Total", width=120, anchor="e")
        tabla.column("Productos", width=100, anchor="center")
        tabla.column("Detalle", width=350, anchor="w")

        tabla.pack(fill="both", expand=True)

        for row in historial:
            tabla.insert(
                "",
                "end",
                values=(
                    row["fecha"],
                    f"${row['total']:,.0f}".replace(",", "."),
                    row["productos"],
                    row["productos_nombres"][:80] + ("..." if len(row["productos_nombres"]) > 80 else "")
                )
            )

    def buscar_productos(self):
        termino = self.entry_busqueda.get().strip()
        productos = VentasController.obtener_productos_para_venta(termino)
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        for p in productos:
            self.tree_productos.insert(
                "",
                "end",
                values=(p["codigo"], p["nombre"], p["stock"], formatear_precio(p["precio"])),
                tags=(p["id"],)
            )

    def centrar_ventana(self, ventana):
        ventana.update_idletasks()
        ancho = ventana.winfo_width()
        alto = ventana.winfo_height()
        root = ventana.master.winfo_toplevel()
        x_root = root.winfo_x()
        y_root = root.winfo_y()
        ancho_root = root.winfo_width()
        alto_root = root.winfo_height()
        x = x_root + (ancho_root // 2) - (ancho // 2)
        y = y_root + (alto_root // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def agregar_al_carrito(self):
        seleccion = self.tree_productos.selection()
        if not seleccion:
            messagebox.showwarning("Seleccionar", "Seleccione un producto de la lista")
            return
        item = self.tree_productos.item(seleccion[0])
        producto_id = item["tags"][0]
        nombre = item["values"][1]
        stock = item["values"][2]
        precio_str = item["values"][3].replace("$", "").replace(".", "")
        precio = float(precio_str)

        ventana_cant = tk.Toplevel(self.contenedor)
        ventana_cant.title("Cantidad")
        ventana_cant.geometry("300x220")
        ventana_cant.resizable(False, False)
        ventana_cant.configure(bg="#f0f2f5")
        ventana_cant.grab_set()
        self.centrar_ventana(ventana_cant)

        tk.Label(
            ventana_cant,
            text=f"Producto: {nombre}",
            font=("Segoe UI", 11, "bold"),
            bg="#f0f2f5",
            fg="#1a237e"
        ).pack(pady=(15, 5))

        tk.Label(
            ventana_cant,
            text=f"Stock disponible: {stock}",
            font=("Segoe UI", 10),
            bg="#f0f2f5",
            fg="#555"
        ).pack()

        tk.Label(
            ventana_cant,
            text="Cantidad:",
            font=("Segoe UI", 10),
            bg="#f0f2f5"
        ).pack(pady=(10, 2))

        entry_cant = tk.Entry(
            ventana_cant,
            font=("Segoe UI", 11),
            width=10,
            justify="center",
            relief="flat",
            highlightthickness=1,
            highlightcolor="#1a237e"
        )
        entry_cant.pack(pady=5)
        entry_cant.focus_set()

        def confirmar():
            try:
                cant = int(entry_cant.get())
                if cant <= 0:
                    raise ValueError
                if cant > stock:
                    messagebox.showerror("Error", "Cantidad excede el stock disponible")
                    return
                for item_carrito in self.carrito:
                    if item_carrito["producto_id"] == producto_id:
                        item_carrito["cantidad"] += cant
                        self.actualizar_carrito()
                        ventana_cant.destroy()
                        return
                self.carrito.append({
                    "producto_id": producto_id,
                    "nombre": nombre,
                    "cantidad": cant,
                    "precio_unitario": precio
                })
                self.actualizar_carrito()
                ventana_cant.destroy()
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")

        frame_botones = tk.Frame(ventana_cant, bg="#f0f2f5")
        frame_botones.pack(pady=15)

        btn_aceptar = tk.Button(
            frame_botones,
            text="Aceptar",
            command=confirmar,
            bg="#43A047",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2"
        )
        btn_aceptar.pack(side="left", padx=10)

        btn_cancelar = tk.Button(
            frame_botones,
            text="Cancelar",
            command=ventana_cant.destroy,
            bg="#78909C",
            fg="white",
            font=("Segoe UI", 10),
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2"
        )
        btn_cancelar.pack(side="left", padx=10)

        ventana_cant.bind("<Return>", lambda event: confirmar())

    def eliminar_del_carrito(self):
        seleccion = self.tree_carrito.selection()
        if not seleccion:
            messagebox.showwarning("Seleccionar", "Seleccione un item del carrito")
            return
        item = self.tree_carrito.item(seleccion[0])
        nombre = item["values"][0]
        precio = float(item["values"][2].replace("$", "").replace(".", ""))
        for i, car in enumerate(self.carrito):
            if car["nombre"] == nombre and car["precio_unitario"] == precio:
                del self.carrito[i]
                break
        self.actualizar_carrito()

    def actualizar_carrito(self):
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)

        subtotal = 0.0
        for item in self.carrito:
            sub = item["cantidad"] * item["precio_unitario"]
            subtotal += sub
            self.tree_carrito.insert(
                "",
                "end",
                values=(
                    item["nombre"],
                    item["cantidad"],
                    formatear_precio(item["precio_unitario"]),
                    formatear_precio(sub)
                )
            )

        total = subtotal
        self.label_subtotal.config(text=f"Subtotal: {formatear_precio(subtotal)}")
        self.label_total.config(text=f"Total: {formatear_precio(total)}")

    def finalizar_venta(self):
        if not self.carrito:
            messagebox.showwarning("Carrito vacío", "No hay productos en el carrito")
            return

        if not self.cliente_seleccionado:
            messagebox.showwarning("Cliente", "Seleccione un cliente.")
            return

        if not messagebox.askyesno("Confirmar venta", "¿Registrar esta venta?"):
            return

        try:
            from models.cliente import Cliente
            cliente = Cliente.obtener_por_id(self.cliente_seleccionado)
            
            # Guardar los IDs de los productos vendidos antes de la venta
            productos_ids = [item["producto_id"] for item in self.carrito]
            
            items = []
            for item in self.carrito:
                items.append({
                    "producto_id": item["producto_id"],
                    "cantidad": item["cantidad"],
                    "precio_unitario": item["precio_unitario"]
                })
            
            venta_id, factura_id, numero_factura = VentasController.realizar_venta(
                self.usuario_id, items, self.cliente_seleccionado
            )
            
            messagebox.showinfo(
                "Venta registrada", 
                f"✅ Venta #{venta_id} realizada con éxito.\n"
                f"📄 Factura: {numero_factura}\n"
                f"👤 Cliente: {cliente['nombre']}"
            )
            
            self.carrito.clear()
            self.actualizar_carrito()
            self.buscar_productos()
            
            # Verificar stock solo de los productos vendidos
            self.verificar_stock_despues_venta(productos_ids)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la venta: {e}")

    def verificar_stock_despues_venta(self, productos_ids):
        """
        Verifica si los productos vendidos quedaron por debajo del stock mínimo.
        Solo muestra alerta si algún producto vendido está bajo el mínimo.
        """
        from models.notificacion import Notificacion
        
        if not productos_ids:
            return
        
        # Verificar solo los productos vendidos
        productos_bajos = Notificacion.verificar_productos_especificos(productos_ids)
        
        if productos_bajos:
            mensaje = "⚠️ ALERTA: Los siguientes productos quedaron con stock bajo\n\n"
            for p in productos_bajos[:5]:
                mensaje += f"• {p['nombre']}: {p['stock']} (mínimo: {p['stock_minimo']}) - Faltan {p['faltante']}\n"
            
            if len(productos_bajos) > 5:
                mensaje += f"\n... y {len(productos_bajos) - 5} más"
            
            messagebox.showwarning("⚠️ Stock Bajo", mensaje)